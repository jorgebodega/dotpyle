import click

from dotpyle.commands.add.dotfile import dotfile


@click.group()
def add():
    """
    This command will take KEY and ... DOTFILE
    """


add.add_command(dotfile)
