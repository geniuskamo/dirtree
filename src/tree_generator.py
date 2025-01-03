import logging
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import lru_cache
from typing import Dict, List, Set

from tqdm import tqdm

from src.formatters import (ConsoleFormatter, JSONFormatter, MarkdownFormatter,
                            TreeFormatter)


class DirectoryTree:
    def __init__(
        self,
        root_dir: str,
        formatter: TreeFormatter = None,
        exclude: List[str] = None,
        follow_symlinks: bool = False,
        max_workers: int = 4,
        cache_size: int = 1000,
    ):
        self.root_dir = root_dir
        self.formatter = formatter or ConsoleFormatter()
        self.exclude = exclude or []
        self.follow_symlinks = follow_symlinks
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"Initializing DirectoryTree for: {root_dir}")
        self.logger.debug(f"Using formatter: {formatter.__class__.__name__}")
        self.logger.debug(f"Exclusion patterns: {exclude}")
        self.logger.debug(f"Follow symlinks: {follow_symlinks}")
        self.total_files = 0
        self.progress = None
        self.max_workers = max_workers
        self._cache: Dict[str, Set[str]] = {}
        self._scanned_dirs = set()

    def _count_entries(self, path: str) -> int:
        """Count total files and directories in a directory."""
        count = 0
        try:
            with os.scandir(path) as it:
                for entry in it:
                    if entry.is_dir(follow_symlinks=False):
                        count += 1
                        count += self._count_entries(entry.path)
                    else:
                        count += 1
        except PermissionError:
            self.logger.error(f"Permission denied accessing directory: {path}")
        return count

    @lru_cache(maxsize=1000)
    def _is_excluded(self, path: str) -> bool:
        """Cached check for excluded paths."""
        return any(
            os.path.commonpath([path, os.path.join(self.root_dir, ex)])
            == os.path.join(self.root_dir, ex)
            for ex in self.exclude
        )

    def _scan_directory(self, path: str) -> List[str]:
        """Optimized directory scanning with caching."""
        if path in self._cache:
            return self._cache[path]

        try:
            with os.scandir(path) as it:
                entries = sorted(entry.name for entry in it)
                self._cache[path] = entries
                return entries
        except PermissionError:
            self.logger.error(f"Permission denied accessing directory: {path}")
            return []

    def generate(self) -> List[str]:
        self.logger.info(f"Starting tree generation for: {self.root_dir}")
        self.total_files = self._count_entries(self.root_dir)
        self.progress = tqdm(
            total=self.total_files,
            desc="Generating tree",
            unit="files",
            disable=None,  # Will respect tqdm.disable environment variable
        )

        tree = []
        if isinstance(self.formatter, MarkdownFormatter):
            self.logger.debug("Using Markdown format")
            tree.append(self.formatter.get_header())
        if isinstance(self.formatter, JSONFormatter):
            self.logger.debug("Using JSON format")
            self._generate_tree(self.root_dir, [], tree)
            self.progress.close()
            return [self.formatter.get_output()]
        self._generate_tree(self.root_dir, "", tree)
        if isinstance(self.formatter, MarkdownFormatter):
            tree.append(self.formatter.get_footer())
        self.logger.info("Tree generation completed successfully")
        self.progress.close()

        # Clear caches after generation
        self._cache.clear()
        self._is_excluded.cache_clear()
        self._scanned_dirs.clear()

        return tree

    def _generate_tree(
        self, current_path: str, prefix: str, tree: List[str]
    ) -> List[str]:
        """Modified to return a list for parallel processing."""
        if not os.path.lexists(
            current_path
        ):  # Use lexists to check for broken symlinks
            self.logger.error(f"Path does not exist: {current_path}")
            return []

        self.progress.update(1)
        result = []
        base_name = os.path.basename(current_path)
        if base_name in self.exclude:
            self.logger.info(f"Skipping excluded path: {base_name}")
            return result

        is_symlink = os.path.islink(current_path)
        is_dir = os.path.isdir(current_path)

        if is_symlink:
            link_target = os.readlink(current_path)
            symlink_exists = os.path.exists(current_path)
            self.logger.debug(f"Found symlink: {current_path} -> {link_target}")

            if base_name:
                line = self.formatter.format_line(
                    prefix, f"{base_name} -> {link_target}", False
                )
                if not symlink_exists:
                    line = self.formatter.format_broken_link(line)
                result.append(line)
                self.logger.debug(f"Added symlink to tree: {base_name}")

            if is_dir and self.follow_symlinks and symlink_exists:
                self._process_directory_parallel(current_path, prefix, result)
        else:
            if base_name:
                result.append(self.formatter.format_line(prefix, base_name, False))
                self.logger.debug(f"Added node to tree: {base_name}")

            if is_dir:
                self._process_directory_parallel(current_path, prefix, result)

        if isinstance(self.formatter, JSONFormatter):
            path_parts = prefix + [base_name]
            self.formatter.add_entry(path_parts, os.path.isdir(current_path))
            self.logger.debug(f"Added JSON entry: {'/'.join(path_parts)}")

        return result

    def _process_directory(
        self, current_path: str, prefix: str, tree: List[str]
    ) -> None:
        try:
            self.logger.debug(f"Processing directory: {current_path}")
            entries = sorted(os.listdir(current_path))
            for i, entry in enumerate(entries):
                entry_path = os.path.join(current_path, entry)
                if any(
                    os.path.commonpath([entry_path, os.path.join(self.root_dir, ex)])
                    == os.path.join(self.root_dir, ex)
                    for ex in self.exclude
                ):
                    self.logger.debug(f"Skipping excluded path: {entry_path}")
                    continue
                is_last = i == len(entries) - 1
                if isinstance(prefix, list):
                    new_prefix = prefix + [entry]
                else:
                    new_prefix = prefix + ("    " if is_last else "│   ")
                self._generate_tree(entry_path, new_prefix, tree)
        except PermissionError:
            self.logger.error(f"Permission denied accessing directory: {current_path}")
            tree.append(self.formatter.format_line(prefix, "<Permission Denied>", True))
        except Exception as e:
            self.logger.critical(
                f"Unexpected error processing directory {current_path}: {str(e)}"
            )
            raise

    def _process_directory_parallel(
        self, current_path: str, prefix: str, tree: List[str]
    ) -> None:
        """Process large directories in parallel."""
        entries = self._scan_directory(current_path)
        if len(entries) > 100:  # Only parallelize for large directories
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                futures = []
                for i, entry in enumerate(entries):
                    entry_path = os.path.join(current_path, entry)
                    if self._is_excluded(entry_path):
                        continue
                    is_last = i == len(entries) - 1
                    new_prefix = prefix + ("    " if is_last else "│   ")
                    futures.append(
                        executor.submit(self._generate_tree, entry_path, new_prefix, [])
                    )

                for future in as_completed(futures):
                    if future.result():
                        tree.extend(future.result())
        else:
            self._process_directory(current_path, prefix, tree)
