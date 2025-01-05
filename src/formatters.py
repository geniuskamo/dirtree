import json
from abc import ABC, abstractmethod
from typing import List
import csv
import xml.etree.ElementTree as ET
from html import escape


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


class XMLFormatter(TreeFormatter):
    def __init__(self):
        self.root = ET.Element("directory")

    def format_line(self, prefix: str, name: str, is_last: bool) -> str:
        # XML formatter does not use this method
        pass

    def add_entry(self, path: List[str], is_dir: bool, symlink_target: str = None):
        current = self.root
        for part in path:
            found = False
            for child in current:
                if child.tag == "directory" and child.attrib["name"] == part:
                    current = child
                    found = True
                    break
            if not found:
                new_elem = ET.SubElement(current, "directory" if is_dir else "file", name=part)
                current = new_elem

    def get_output(self) -> str:
        return ET.tostring(self.root, encoding="unicode")


class HTMLFormatter(TreeFormatter):
    def __init__(self):
        self.lines = []

    def format_line(self, prefix: str, name: str, is_last: bool) -> str:
        indent = len(prefix) * "&nbsp;&nbsp;&nbsp;&nbsp;"
        return f"{indent}{'└── ' if is_last else '├── '}{escape(name)}<br>"

    def add_entry(self, path: List[str], is_dir: bool, symlink_target: str = None):
        # HTML formatter does not use this method
        pass

    def get_output(self) -> str:
        return "<html><body>" + "".join(self.lines) + "</body></html>"


class CSVFormatter(TreeFormatter):
    def __init__(self):
        self.rows = []

    def format_line(self, prefix: str, name: str, is_last: bool) -> str:
        # CSV formatter does not use this method
        pass

    def add_entry(self, path: List[str], is_dir: bool, symlink_target: str = None):
        self.rows.append(path)

    def get_output(self) -> str:
        output = []
        writer = csv.writer(output)
        writer.writerows(self.rows)
        return "\n".join(output)


class PlainTextFormatter(TreeFormatter):
    def format_line(self, prefix: str, name: str, is_last: bool) -> str:
        return f"{prefix}{'└── ' if is_last else '├── '}{name}"

    def add_entry(self, path: List[str], is_dir: bool, symlink_target: str = None):
        # Plain text formatter does not use this method
        pass

    def get_output(self) -> str:
        # Plain text formatter does not use this method
        pass
