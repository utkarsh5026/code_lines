import rich_click as click
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from cmd.line_count import LineCountCommand

# Enhance rich_click configuration
click.rich_click.USE_RICH_MARKUP = True
click.rich_click.GROUP_ARGUMENTS_OPTIONS = True
click.rich_click.STYLE_ERRORS_SUGGESTION = "yellow italic"
click.rich_click.STYLE_OPTIONS_HELP_PREFIX = "cyan"
click.rich_click.STYLE_USAGE = "green bold"

console = Console()


@click.group()
def cli():
    """[bold cyan]📊 Line Counter[/]

    A powerful CLI tool for counting lines of code in your projects.
    """


@cli.command(name="cl")
@click.option(
    '--root-dir', '-d',
    default=".",
    help="[green]Root directory to analyze[/] [dim](default: current directory)[/]"
)
@click.option(
    '--extensions', '-e',
    multiple=True,
    help="[green]File extensions to count[/] [dim](e.g., -e py -e js)[/]"
)
@click.option(
    '--ignore', '-i',
    multiple=True,
    help="[green]Patterns to ignore[/] [dim](e.g., -i '**/venv/**' -i '**/.git/**')[/]"
)
@click.option(
    '--file-wise', '-f',
    is_flag=True,
    help="[green]Count lines per file[/]"
)
@click.option(
    '--directory-wise', '-d',
    is_flag=True,
    help="[green]Count lines per directory[/]"
)
def count_lines(root_dir: str, extensions: tuple[str], ignore: tuple[str], file_wise: bool, directory_wise: bool):
    """[bold]Count lines of code in the specified directory.[/]

    📁 Analyzes your codebase and provides detailed line counts."""

    console.print(Panel.fit(
        Text("Starting analysis...", style="bold blue"),
        border_style="blue"
    ))

    LineCountCommand(
        console=console,
        root_dir=root_dir,
        extensions=list(extensions) if extensions else None,
        ignore_patterns=list(ignore) if ignore else None,
        file_wise=file_wise,
        directory_wise=directory_wise
    ).run()


if __name__ == "__main__":
    cli()
