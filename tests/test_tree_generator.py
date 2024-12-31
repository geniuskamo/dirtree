import os
from src.tree_generator import DirectoryTree
from src.formatters import ConsoleFormatter, MarkdownFormatter

def test_directory_tree_with_console_formatter(temp_dir):
    tree = DirectoryTree(temp_dir, ConsoleFormatter())
    result = tree.generate()
    
    assert len(result) > 0
    assert any("dir1" in line for line in result)
    assert any("subdir1" in line for line in result)
    assert any("file1.txt" in line for line in result)

def test_directory_tree_with_markdown_formatter(temp_dir):
    tree = DirectoryTree(temp_dir, MarkdownFormatter())
    result = tree.generate()
    
    assert result[0] == "# Directory Structure\n"
    assert result[-1] == "```\n"
    assert any("&nbsp;" in line for line in result)

def test_directory_tree_with_empty_directory(empty_dir):
    tree = DirectoryTree(empty_dir)
    result = tree.generate()
    assert len(result) == 1
