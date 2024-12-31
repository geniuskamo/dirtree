import os
import pytest
from src.cli import main
from unittest.mock import patch
import sys

def test_cli_with_directory(temp_dir, capsys):
    with patch.object(sys, 'argv', ['dirtree', temp_dir]):
        main()
        captured = capsys.readouterr()
        assert "dir1" in captured.out
        assert "file1.txt" in captured.out

def test_cli_markdown_output(temp_dir, tmp_path):
    output_file = tmp_path / "output.md"
    with patch.object(sys, 'argv', [
        'dirtree', temp_dir, 
        '--format', 'markdown',
        '-o', str(output_file)
    ]):
        main()
        assert output_file.exists()
        content = output_file.read_text()
        assert "# Directory Structure" in content
