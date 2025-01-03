import os
import logging
from typing import List
from src.formatters import TreeFormatter, ConsoleFormatter, MarkdownFormatter, JSONFormatter

class DirectoryTree:
    def __init__(self, root_dir: str, formatter: TreeFormatter = None, exclude: List[str] = None):
        self.root_dir = root_dir
        self.formatter = formatter or ConsoleFormatter()
        self.exclude = exclude or []
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"Initializing DirectoryTree for: {root_dir}")
        self.logger.debug(f"Using formatter: {formatter.__class__.__name__}")
        self.logger.debug(f"Exclusion patterns: {exclude}")

    def generate(self) -> List[str]:
        self.logger.info(f"Starting tree generation for: {self.root_dir}")
        tree = []
        if isinstance(self.formatter, MarkdownFormatter):
            self.logger.debug("Using Markdown format")
            tree.append(self.formatter.get_header())
        if isinstance(self.formatter, JSONFormatter):
            self.logger.debug("Using JSON format")
            self._generate_tree(self.root_dir, [], tree)
            return [self.formatter.get_output()]
        self._generate_tree(self.root_dir, "", tree)
        if isinstance(self.formatter, MarkdownFormatter):
            tree.append(self.formatter.get_footer())
        self.logger.info("Tree generation completed successfully")
        return tree

    def _generate_tree(self, current_path: str, prefix: str, tree: List[str]) -> None:
        if not os.path.exists(current_path):
            self.logger.error(f"Path does not exist: {current_path}")
            return

        base_name = os.path.basename(current_path)
        if base_name in self.exclude:
            self.logger.info(f"Skipping excluded directory: {base_name}")
            return

        if base_name:
            tree.append(self.formatter.format_line(prefix, base_name, False))
            self.logger.debug(f"Added node to tree: {base_name}")

        if os.path.isdir(current_path):
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
        if isinstance(self.formatter, JSONFormatter):
            path_parts = prefix + [base_name]
            self.formatter.add_entry(path_parts, os.path.isdir(current_path))
            self.logger.debug(f"Added JSON entry: {'/'.join(path_parts)}")
