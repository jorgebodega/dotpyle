import click
import subprocess
from git import Repo
from os import mkdir, path, sys
from shutil import rmtree
from dotpyle.utils import get_default_path, get_default_url

from dotpyle.services.config_handler import ConfigHandler
from dotpyle.services.config_parser import ConfigParser


parser = ConfigParser(config=ConfigHandler().get_config())


@click.group()
# dotpyle init.vim --key vim
# dotpyle add <key> <dotfile>
# dotpyle add <key> <dotfile>:<path>
def add():
    """
    This command will take KEY and ... DOTFILE
    """
    pass


# FIXME: when config file is empty, an error is returned
# TypeError: argument of type 'NoneType' is not iterable
@add.command()
@click.help_option(help="Add file to dotpyles")
@click.argument("name")
@click.option("--profile", "-p", default="default", help="Profile name, must exist")
@click.option("--root", "-r", default="~", help="Root path")
@click.option(
    "--path", multiple=True, help="Program dotfiles paths starting from root path"
)
# @click.option("--pre-hook", multiple=True,  help="Program dotfiles paths starting from root path")
def dotfile(name, profile, root, path):
    """ Add DOTFILE to KEY group on Dotpyle tracker TBD """
    print(name, profile, root, path)
    # Convert path touple to list
    paths = [p for p in path]
    parser.add_dotfile(name, profile, root, paths, pre_hooks=None, post_hooks=None)
