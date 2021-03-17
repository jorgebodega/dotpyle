import click

from dotpyle.commands.init import init
from dotpyle.commands.help import help
from dotpyle.commands.add import add
from dotpyle.commands.list import list
from dotpyle.commands.config import config


@click.group()
def dotpyle():
    """ Needed to create different commands with different options """
    pass


@click.command()
def commit():
    pass




# Add commands to group
dotpyle.add_command(init)
dotpyle.add_command(add)
dotpyle.add_command(commit)
dotpyle.add_command(config)
dotpyle.add_command(help)
dotpyle.add_command(list)
dotpyle.add_command(config)



def main():
    dotpyle()


if __name__ == "__main__":
    dotpyle()
