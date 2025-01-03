from abc import ABC, abstractmethod
from typing import List
import json

class TreeFormatter(ABC):
    @abstractmethod
    def format_line(self, prefix: str, name: str, is_last: bool) -> str:
        pass

    def format_broken_link(self, line: str) -> str:
        """Format a broken symlink line."""
        return f"{line} [broken]"

class ConsoleFormatter(TreeFormatter):
    def format_line(self, prefix: str, name: str, is_last: bool) -> str:
        return f"{prefix}{'└── ' if is_last else '├── '}{name}"

class MarkdownFormatter(TreeFormatter):
    def format_line(self, prefix: str, name: str, is_last: bool) -> str:
        indent = prefix.replace("│", "|").replace(" ", "    ")
        return f"{indent}{'└── ' if is_last else '├── '}{name}"

    def get_header(self) -> str:
        return "# Directory Structure\n"

    def get_footer(self) -> str:
        return "```\n"

    def format_broken_link(self, line: str) -> str:
        return f"{line} *[broken]*"

class JSONFormatter(TreeFormatter):
    def __init__(self):
        self.tree = {}
        self.symlinks = {}

    def format_line(self, prefix: str, name: str, is_last: bool) -> str:
        # JSON formatter does not use this method
        pass

    def add_entry(self, path: List[str], is_dir: bool, symlink_target: str = None):
        current = self.tree
        for part in path[:-1]:
            current = current.setdefault(part, {})
        if symlink_target:
            current[path[-1]] = {"type": "symlink", "target": symlink_target}
        else:
            current[path[-1]] = {} if is_dir else None

    def get_output(self) -> str:
        return json.dumps(self.tree, indent=4)
