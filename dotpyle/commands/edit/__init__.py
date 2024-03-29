import click

from dotpyle.commands.edit.config import config
from dotpyle.commands.edit.local import local
from dotpyle.commands.edit.readme import readme


@click.group()
def edit():
    """Manually edit Dotpyle internal files"""
    pass


edit.add_command(config)
edit.add_command(readme)
edit.add_command(local)
