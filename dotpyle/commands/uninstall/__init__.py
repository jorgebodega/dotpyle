import click

from dotpyle.commands.uninstall.dotfile import dotfile


@click.group()
def uninstall():
    """
    Uninstall a dotfile, hook, etc (TBD)
    """


uninstall.add_command(dotfile)
