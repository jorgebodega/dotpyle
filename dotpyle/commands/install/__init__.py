import click

from dotpyle.commands.install.dotfile import dotfile


@click.group()
def install():
    """
    Install a dotfile, hook, etc (TBD)
    """


install.add_command(dotfile)
