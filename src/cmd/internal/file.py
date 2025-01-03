from pathlib import Path
import fnmatch


def get_files_to_process(root_dir: str,
                         extensions: list[str],
                         ignore_patterns: list[str]) -> list[Path]:
    """
    Get the list of files to process based on extensions and ignore patterns.

    Args:
        root_dir (str): The root directory to search for files
        extensions (list[str]): List of file extensions to include (without dot)
        ignore_patterns (list[str]): List of glob patterns to ignore

    Returns:
        list[Path]: List of Path objects for matching files

    Raises:
        FileNotFoundError: If the root directory does not exist

    Example:
        >>> files = get_files_to_process(
        ...     "src",
        ...     extensions=["py", "js"],
        ...     ignore_patterns=["**/test/**", "**/__pycache__/**"]
        ... )
    """
    files = set()
    root = Path(root_dir).resolve()

    if not root.exists():
        raise FileNotFoundError(f"The directory {root_dir} does not exist")

    for ext in extensions:
        for file_path in root.rglob(f"*.{ext}"):
            should_ignore = any(
                fnmatch.fnmatch(str(file_path), pattern)
                for pattern in ignore_patterns
            )
            if not should_ignore:
                files.add(file_path)

    return list(files)


def count_lines_in_file(file_path: Path) -> int:
    """
    Count the lines in a file.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return sum(1 for _ in file)
