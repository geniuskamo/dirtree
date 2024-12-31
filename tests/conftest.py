import os
import pytest
import tempfile
import shutil

@pytest.fixture
def temp_dir():
    """Create a temporary directory structure for testing."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        # Create a test directory structure
        os.makedirs(os.path.join(tmp_dir, "dir1/subdir1"))
        os.makedirs(os.path.join(tmp_dir, "dir1/subdir2"))
        open(os.path.join(tmp_dir, "dir1/file1.txt"), "w").close()
        open(os.path.join(tmp_dir, "dir1/subdir1/file2.txt"), "w").close()
        yield tmp_dir

@pytest.fixture
def empty_dir():
    """Create an empty temporary directory."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield tmp_dir
