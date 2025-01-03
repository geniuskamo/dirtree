from src.formatters import ConsoleFormatter, MarkdownFormatter, JSONFormatter
from src.tree_generator import DirectoryTree

def test_console_formatter():
    formatter = ConsoleFormatter()
    result = formatter.format_line("    ", "test.txt", False)
    assert result == "    ├── test.txt"
    
    result = formatter.format_line("    ", "test.txt", True)
    assert result == "    └── test.txt"

def test_markdown_formatter():
    formatter = MarkdownFormatter()
    result = formatter.format_line("│   ", "test.txt", False)
    assert "    " in result
    assert "├── test.txt" in result
    
    assert formatter.get_header().startswith("# Directory")
    assert formatter.get_footer() == "```\n"

def test_exclude_directories(temp_dir):
    formatter = ConsoleFormatter()
    tree = DirectoryTree(temp_dir, formatter, exclude=["dir1/subdir1"])
    result = tree.generate()
    assert "subdir1" not in "\n".join(result)

def test_json_formatter():
    formatter = JSONFormatter()
    formatter.add_entry(["dir1"], True)
    formatter.add_entry(["dir1", "file1.txt"], False)
    result = formatter.get_output()
    assert '"dir1": {' in result
    assert '"file1.txt": null' in result
