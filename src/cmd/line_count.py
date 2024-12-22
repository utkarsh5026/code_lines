from pathlib import Path
from typing import Optional
from collections import defaultdict

from rich.console import Console
from rich.progress import track
from rich.panel import Panel
from rich.table import Table
from rich import box

from .base import BaseCommand
from .internal import get_files_to_process, count_lines_in_file


class LineCountCommand(BaseCommand):

    def __init__(self, console: Console,
                 root_dir: Optional[str] = None,
                 extensions: Optional[list[str]] = None,
                 ignore_patterns: Optional[list[str]] = None,
                 file_wise: bool = False,
                 directory_wise: bool = False):
        """
        Initialize the LineCountCommand.

        Args:
            console (Console): The console instance.
            root_dir (Optional[str]): The root directory to count lines in.
            extensions (Optional[list[str]]): The file extensions to count.
            ignore_patterns (Optional[list[str]]): The patterns to ignore.
        """
        super().__init__(console)
        self.root_dir = Path(root_dir or ".").resolve()
        self.extensions = extensions or []
        self.ignore_patterns = ignore_patterns or []
        self.file_wise = file_wise
        self.directory_wise = directory_wise

    def __count_total_lines(self, files: list[Path]):
        """
        Count the total lines in the files.
        """
        total_lines = 0
        total_files = len(files)
        for _, file in enumerate(track(files, description="Counting lines...", console=self.console, total=total_files)):
            total_lines += count_lines_in_file(file)

        return total_lines

    def __count_file_wise(self, files: list[Path]):
        """
        Count the lines in the files directory-wise.
        """
        dir_files = defaultdict(list)
        for file in files:
            dir_files[file.parent].append(file)

        table = Table(
            title="Directory-wise Line Count",
            show_lines=False,
            padding=(0, 2),
            box=box.ROUNDED
        )
        table.add_column("Directory", style="cyan")
        table.add_column("File", style="green")
        table.add_column("Lines", justify="left", style="bold white")

        dirs_list = sorted(dir_files.items())

        for i, (directory, dir_files_list) in enumerate(dirs_list):
            first_file = True
            for file in sorted(dir_files_list):
                lines = count_lines_in_file(file)
                try:
                    rel_path = directory.relative_to(self.root_dir)
                    dir_display = str(rel_path)
                except ValueError:
                    dir_display = str(directory)

                table.add_row(
                    dir_display if first_file else "",
                    file.name,
                    str(lines)
                )
                first_file = False

            if i < len(dirs_list) - 1:
                table.add_row("", "", "", style="dim", end_section=True)

        self.console.print(table)

    def __count_directory_wise(self, files: list[Path]):
        """
        Count the lines in the files directory-wise, showing total lines per directory.
        """
        dir_lines = defaultdict(int)
        dir_files = defaultdict(int)

        for file in files:
            lines = count_lines_in_file(file)
            dir_lines[file.parent] += lines
            dir_files[file.parent] += 1

        table = Table(
            title="Directory-wise Summary",
            show_lines=False,
            padding=(0, 2),
            box=box.ROUNDED
        )
        table.add_column("Directory", style="cyan")
        table.add_column("Files", justify="right", style="green")
        table.add_column("Lines", justify="right", style="bold white")

        # Add rows sorted by directory
        total_files = 0
        total_lines = 0
        for directory in sorted(dir_lines.keys()):
            try:
                rel_path = directory.relative_to(self.root_dir)
                dir_display = str(rel_path)
            except ValueError:
                dir_display = str(directory)

            files_count = dir_files[directory]
            lines_count = dir_lines[directory]
            total_files += files_count
            total_lines += lines_count

            table.add_row(
                dir_display,
                str(files_count),
                str(lines_count)
            )

        # Add total row
        table.add_row("", "", "", style="dim", end_section=True)
        table.add_row(
            "[bold]Total",
            f"[bold]{total_files}",
            f"[bold]{total_lines}"
        )

        self.console.print(table)

    def run(self):
        """
        Run the line count command.
        """
        total_lines = 0
        files = get_files_to_process(
            root_dir=self.root_dir,
            extensions=self.extensions,
            ignore_patterns=self.ignore_patterns
        )

        if not self.file_wise and not self.directory_wise:
            total_lines = self.__count_total_lines(files)
            self.console.print(f"Total lines: [bold green]{total_lines}[/]")

        if self.file_wise:
            self.__count_file_wise(files)

        if self.directory_wise:
            self.__count_directory_wise(files)
