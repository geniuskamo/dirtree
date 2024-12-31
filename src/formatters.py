from abc import ABC, abstractmethod
from typing import List


class TreeFormatter(ABC):
    @abstractmethod
    def format_line(self, prefix: str, name: str, is_last: bool) -> str:
        pass


class ConsoleFormatter(TreeFormatter):
    def format_line(self, prefix: str, name: str, is_last: bool) -> str:
        return f"{prefix}{'└── ' if is_last else '├── '}{name}"


class MarkdownFormatter(TreeFormatter):
    def format_line(self, prefix: str, name: str, is_last: bool) -> str:
        indent = prefix.replace("│", "|").replace(
            "    ", "&nbsp;&nbsp;&nbsp;&nbsp;")
        return f"{indent}{'└── ' if is_last else '├── '}{name}"

    def get_header(self) -> str:
        return "# Directory Structure\n\n```\n"

    def get_footer(self) -> str:
        return "```\n"
