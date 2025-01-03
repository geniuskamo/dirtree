import os
import logging
from typing import List
from tqdm import tqdm
from src.formatters import TreeFormatter, ConsoleFormatter, MarkdownFormatter, JSONFormatter

class DirectoryTree:
    def __init__(self, root_dir: str, formatter: TreeFormatter = None, exclude: List[str] = None, follow_symlinks: bool = False):
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

    def _count_entries(self, path: str) -> int:
        """Count total number of entries for progress tracking."""
        count = 0
        try:
            for entry in os.scandir(path):
                count += 1
                if entry.is_dir(follow_symlinks=self.follow_symlinks) and entry.name not in self.exclude:
                    if entry.is_symlink() and not self.follow_symlinks:
                        continue
                    count += self._count_entries(entry.path)
        except PermissionError:
            self.logger.warning(f"Permission denied while counting entries in: {path}")
        return count

    def generate(self) -> List[str]:
        self.logger.info(f"Starting tree generation for: {self.root_dir}")
        self.total_files = self._count_entries(self.root_dir)
        self.progress = tqdm(
            total=self.total_files,
            desc="Generating tree",
            unit="files",
            disable=None  # Will respect tqdm.disable environment variable
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
        return tree

    def _generate_tree(self, current_path: str, prefix: str, tree: List[str]) -> None:
        if not os.path.lexists(current_path):  # Use lexists to check for broken symlinks
            self.logger.error(f"Path does not exist: {current_path}")
            return

        self.progress.update(1)
        base_name = os.path.basename(current_path)
        if base_name in self.exclude:
            self.logger.info(f"Skipping excluded path: {base_name}")
            return

        is_symlink = os.path.islink(current_path)
        is_dir = os.path.isdir(current_path)
        
        if is_symlink:
            link_target = os.readlink(current_path)
            symlink_exists = os.path.exists(current_path)
            self.logger.debug(f"Found symlink: {current_path} -> {link_target}")
            
            if base_name:
                line = self.formatter.format_line(prefix, f"{base_name} -> {link_target}", False)
                if not symlink_exists:
                    line = self.formatter.format_broken_link(line)
                tree.append(line)
                self.logger.debug(f"Added symlink to tree: {base_name}")

            if is_dir and self.follow_symlinks and symlink_exists:
                self._process_directory(current_path, prefix, tree)
        else:
            if base_name:
                tree.append(self.formatter.format_line(prefix, base_name, False))
                self.logger.debug(f"Added node to tree: {base_name}")

            if is_dir:
                self._process_directory(current_path, prefix, tree)

        if isinstance(self.formatter, JSONFormatter):
            path_parts = prefix + [base_name]
            self.formatter.add_entry(path_parts, os.path.isdir(current_path))
            self.logger.debug(f"Added JSON entry: {'/'.join(path_parts)}")

    def _process_directory(self, current_path: str, prefix: str, tree: List[str]) -> None:
        try:
            self.logger.debug(f"Processing directory: {current_path}")
            entries = sorted(os.listdir(current_path))
            for i, entry in enumerate(entries):
                entry_path = os.path.join(current_path, entry)
                if any(os.path.commonpath([entry_path, os.path.join(self.root_dir, ex)]) == os.path.join(self.root_dir, ex) for ex in self.exclude):
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
            self.logger.critical(f"Unexpected error processing directory {current_path}: {str(e)}")
            raise
