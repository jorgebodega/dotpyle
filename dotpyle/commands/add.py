import click
import subprocess
from git import Repo
from os import mkdir, path, sys
from shutil import rmtree
from dotpyle.utils import get_default_path, get_default_url

from dotpyle.services.ConfigHandler import ConfigHandler


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
@click.argument(
    "key",
)
@click.argument(
    "dotfile",
)
def file(key, dotfile):
    """ Add DOTFILE to KEY group on Dotpyle tracker TBD """
    cfh = ConfigHandler()
    config = cfh.read()
    print(config)
    if key in config:
        key_config = config[key]
        if dotfile in key_config:
            print("Existing file on key config")
        else:
            key_config["paths"].append(dotfile)

    else:
        config[key] = {"paths": [dotfile]}

    print("after")
    print(config)
    cfh.save(config)
