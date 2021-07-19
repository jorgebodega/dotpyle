import click
import os
from git.index import base
from dotpyle.services.repo_handler import RepoHandler
from dotpyle.services.file_handler import FileHandler
from dotpyle.services.config_handler import ConfigHandler
from dotpyle.utils.path import get_source_and_link_path


@click.command()
def pull():
    repo = RepoHandler()

    repo.pull()
