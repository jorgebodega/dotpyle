import click

from dotpyle.commands.init import init
from dotpyle.commands.help import help


@click.group()
def dotpyle():
    """ Needed to create different commands with different options """
    pass


@click.command()
@click.option("--path", help="Path file")
def add(path):
    pass


@click.command()
def commit():
    pass


@click.command()
def config():
    pass


# Add commands to group
dotpyle.add_command(init)
dotpyle.add_command(add)
dotpyle.add_command(commit)
dotpyle.add_command(config)
dotpyle.add_command(help)


def main():
    dotpyle()


if __name__ == "__main__":
    dotpyle()
