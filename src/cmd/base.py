from rich.console import Console
from rich.panel import Panel
from abc import ABC, abstractmethod


class BaseCommand(ABC):
    def __init__(self, console: Console):
        """
        Parameters:
        console (Console): Rich Console instance to print output
        """
        self.console = console

    @abstractmethod
    def run(self):
        """
        Abstract method to run the command
        """
        pass

    def error(self, message: str, exception: Exception):
        """
        Print an error message with exception details.

        Parameters:
        message (str): The error message to print
        exception (Exception): The exception to print
        """
        error_content = f"{message}\n\nException Details:\n{str(exception)}"
        self.console.print(Panel(
            error_content,
            title="[red]Error[/red]",
            border_style="red",
            padding=(1, 2)
        ))
