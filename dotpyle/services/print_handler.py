from rich.console import Console

console = Console()


def print(*args):
    console.print(*args, style="bold")
