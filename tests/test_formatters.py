from src.formatters import ConsoleFormatter, MarkdownFormatter

def test_console_formatter():
    formatter = ConsoleFormatter()
    result = formatter.format_line("    ", "test.txt", False)
    assert result == "    ├── test.txt"
    
    result = formatter.format_line("    ", "test.txt", True)
    assert result == "    └── test.txt"

def test_markdown_formatter():
    formatter = MarkdownFormatter()
    result = formatter.format_line("│   ", "test.txt", False)
    assert "&nbsp;" in result
    assert "├── test.txt" in result
    
    assert formatter.get_header().startswith("# Directory")
    assert formatter.get_footer() == "```\n"
