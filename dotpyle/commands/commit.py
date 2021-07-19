import click
import os
from git.index import base
from dotpyle.services.repo_handler import RepoHandler
from dotpyle.services.file_handler import FileHandler
from dotpyle.services.config_handler import ConfigHandler
from dotpyle.utils.path import get_source_and_link_path

# from dotpyle.decorators import init_handlers

from os import walk
from os import listdir
from os.path import isfile, join, isdir
import glob, itertools


@click.command()
@click.option("--name", "-n", default="", help="program name")
@click.option("--profile", "-p", default="default", help="profile name")
@click.option(
    "--path",
    multiple=True,
    help="Program dotfiles paths starting from root path",
)
@click.option("--message", "-m", help="commit message")
# TODO: make path option name dependant
def commit(name: str, profile: str, path: list[str], message: str):
    handler = FileHandler()
    parser = ConfigHandler(config=handler.config)
    repo = RepoHandler()
    # if name == "" and profile == "":
    # key_paths = handler.get_key_paths()
    # repo.add(path=key_paths)
    # print(key_paths)

    # 1. Add files based on parameters
    if name == "":
        for name, profiles in parser.get_names_and_profiles():
            for prof in profiles:
                if profile == "" or profile == prof:
                    for source in parser.get_profile_paths(name, prof):
                        repo.add(paths=source)

    else:
        print("One name")
        # Expand path tuple to list
        paths = [p for p in path]
        for prof in parser.get_profiles_for_name(name):
            if profile == "" or profile == prof:
                for source, _ in parser.get_calculated_paths(name, profile):
                    if profile == "" or paths == [] or source in paths:
                        repo.add(paths=source)

    # 2. Proceed with commit
    repo.commit(message)
