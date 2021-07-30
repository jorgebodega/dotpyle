from rich.console import Console
from rich.text import Text


class Logger:
    def __init__(self, verbose):
        self.verbose = verbose
        if self.verbose:
            self.console = Console(color_system="auto")

    def __print(self, text: Text):
        """
        Prints the message.
        """
        if self.verbose:
            self.console.print(text)

    def log(self, msg):
        """
        Prints a message to the console.
        """
        self.__print(Text(msg))

    def warning(self, msg):
        """
        Prints a warning message to the console.
        """
        self.__print(Text(msg, style="yellow"))

    def error(self, msg):
        """
        Prints an error message to the console.
        """
        self.__print(Text(msg, style="red"))
