from rich.console import Console
from rich.panel import Panel
from abc import ABC, abstractmethod


class BaseCommand(ABC):
    def __init__(self, console: Console):
        self.console = console

    @abstractmethod
    def run(self):
        pass

    def error(self, message: str, exception: Exception):
        error_content = f"{message}\n\nException Details:\n{str(exception)}"
        self.console.print(Panel(
            error_content,
            title="[red]Error[/red]",
            border_style="red",
            padding=(1, 2)
        ))
