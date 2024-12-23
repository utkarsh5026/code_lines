from pathlib import Path
import pytest
from src.cmd.internal import get_files_to_process, count_lines_in_file


def test_count_lines_in_file(tmp_path):
    # Create a temporary file with known content
    test_file = tmp_path / "test.txt"
    test_content = "line1\nline2\nline3\n"
    test_file.write_text(test_content)

    assert count_lines_in_file(test_file) == 3


def test_get_files_to_process(tmp_path):
    # Create test directory structure
    (tmp_path / "dir1").mkdir()
    (tmp_path / "dir2").mkdir()

    # Create test files
    (tmp_path / "file1.py").write_text("content")
    (tmp_path / "dir1" / "file2.py").write_text("content")
    (tmp_path / "dir2" / "file3.py").write_text("content")
    (tmp_path / "file4.txt").write_text("content")
    (tmp_path / "dir1" / "ignore_me.py").write_text("content")

    # Test basic file collection
    files = get_files_to_process(
        str(tmp_path),
        extensions=["py"],
        ignore_patterns=[]
    )
    assert len(files) == 4
    assert all(f.suffix == ".py" for f in files)

    # Test with ignore patterns
    files = get_files_to_process(
        str(tmp_path),
        extensions=["py"],
        ignore_patterns=["**/ignore_me.py"]
    )
    assert len(files) == 3
    assert not any(f.name == "ignore_me.py" for f in files)

    # Test multiple extensions
    files = get_files_to_process(
        str(tmp_path),
        extensions=["py", "txt"],
        ignore_patterns=[]
    )
    assert len(files) == 5

    # Test non-existent extension
    files = get_files_to_process(
        str(tmp_path),
        extensions=["jpg"],
        ignore_patterns=[]
    )
    assert len(files) == 0


def test_get_files_to_process_with_invalid_dir():
    with pytest.raises(Exception):
        get_files_to_process(
            "non_existent_directory",
            extensions=["py"],
            ignore_patterns=[]
        )
