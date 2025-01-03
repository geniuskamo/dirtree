from abc import ABC, abstractmethod
from typing import List
import json

class TreeFormatter(ABC):
    @abstractmethod
    def format_line(self, prefix: str, name: str, is_last: bool) -> str:
        pass


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


class JSONFormatter(TreeFormatter):
    def __init__(self):
        self.tree = {}

    def format_line(self, prefix: str, name: str, is_last: bool) -> str:
        # JSON formatter does not use this method
        pass

    def add_entry(self, path: List[str], is_dir: bool):
        current = self.tree
        for part in path[:-1]:
            current = current.setdefault(part, {})
        current[path[-1]] = {} if is_dir else None

    def get_output(self) -> str:
        return json.dumps(self.tree, indent=4)
