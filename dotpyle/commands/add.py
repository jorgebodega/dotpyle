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


@click.group()
def add():
    """
    This command will take KEY and ... DOTFILE
    """
    pass


# FIXME: when config file is empty, an error is returned
# TypeError: argument of type 'NoneType' is not iterable
@add.command()
@click.help_option(help="Add file to dotpyle")
@click.argument("name")
@click.option("--profile", "-p", default="default", help="Profile name, must exist")
@click.option("--root", "-r", default="~", help="Root path")
@click.option(
    "--path",
    multiple=True,
    help="Program dotfiles paths starting from root path",
)
# TODO: make this optional and add everything inside root
@click.option(
    "--pre",
    multiple=True,
    help="Bash command(s) to be executed before installing configuration",
)
@click.option(
    "--post",
    multiple=True,
    help="Bash command(s) to be executed after installing configuration",
)
@click.option(
    "--not-install",
    default=False,
    is_flag=True,
    help="Add files to Dotpyle repo and remove them from original location (useful if user wants to install it afterwards, see dotpyle install)",
)
# @click.option("--pre-hook", multiple=True,  help="Program dotfiles paths starting from root path")
def dotfile(name, profile, root, path, pre, post, not_install):
    """ Add DOTFILE to KEY group on Dotpyle tracker TBD """
    handler = FileHandler()
    parser = ConfigHandler(config=handler.config)
    repo = RepoHandler()
    print(name, profile, root, path, pre, post)
    # Convert tuples to lists
    paths = [p for p in path]
    pre_commands = [p for p in pre]
    post_commands = [p for p in post]
    added_paths = parser.add_dotfile(
        name,
        profile,
        root,
        paths,
        pre_hooks=pre_commands,
        post_hooks=post_commands,
    )

    # Save modified dotpyle config file
    handler.save(parser.config)
    # When new key is added to dotpyle, a commit should be generated
    # (adding new files), to keep consistency between yaml and repo

    repo.add(added_paths, config_file_changed=True)
    commit_message = "[dotpyle]: added {} on {} profile on {} program".format(
        added_paths, profile, name
    )
    repo.commit(commit_message)

    if not not_install:
        local_handler = LocalFileHandler()
        local_handler.install_profile(name, profile)
        local_handler.save()

        parser.install_key(
            key_name=name, profile_name=profile, process_pre=False, process_post=False
        )
