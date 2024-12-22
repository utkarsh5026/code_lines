from pathlib import Path
import fnmatch


def get_files_to_process(root_dir: str,
                         extensions: list[str],
                         ignore_patterns: list[str]) -> list[Path]:
    """
    Get the list of files to process.
    """
    files = set()
    root = Path(root_dir).resolve()

    print(root, extensions, ignore_patterns)

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
