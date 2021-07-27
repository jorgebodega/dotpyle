import click
import subprocess
from git import Repo
from os import mkdir, path, sys
from shutil import rmtree
from dotpyle.utils.path import get_default_path
from dotpyle.utils.url import get_default_url

from dotpyle.services.file_handler import FileHandler, LocalFileHandler
from dotpyle.services.config_handler import ConfigHandler
from dotpyle.services.repo_handler import RepoHandler

@click.command()
@click.help_option(help="Add/edit script in order to execute it later")
@click.argument("name")
def script(name):
    """Add/edit script in order to execute it later"""
    handler = FileHandler()
    parser = ConfigHandler(config=handler.config)

    pass

