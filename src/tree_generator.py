import os
from typing import List
from src.formatters import TreeFormatter, ConsoleFormatter, MarkdownFormatter


class DirectoryTree:
    def __init__(self, root_dir: str, formatter: TreeFormatter = None):
        self.root_dir = root_dir
        self.formatter = formatter or ConsoleFormatter()

    def generate(self) -> List[str]:
        tree = []
        if isinstance(self.formatter, MarkdownFormatter):
            tree.append(self.formatter.get_header())
        self._generate_tree(self.root_dir, "", tree)
        if isinstance(self.formatter, MarkdownFormatter):
            tree.append(self.formatter.get_footer())
        return tree

    def _generate_tree(self, current_path: str, prefix: str, tree: List[str]) -> None:
        if not os.path.exists(current_path):
            return

        base_name = os.path.basename(current_path)
        if base_name:
            tree.append(self.formatter.format_line(prefix, base_name, False))

        if os.path.isdir(current_path):
            try:
                entries = sorted(os.listdir(current_path))
                for i, entry in enumerate(entries):
                    is_last = i == len(entries) - 1
                    new_prefix = prefix + ("    " if is_last else "│   ")
                    entry_path = os.path.join(current_path, entry)
                    self._generate_tree(entry_path, new_prefix, tree)
            except PermissionError:
                tree.append(self.formatter.format_line(
                    prefix, "<Permission Denied>", True))
