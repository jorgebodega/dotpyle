import click
from git.index import base
from dotpyle.services.repo_handler import RepoHandler
from dotpyle.services.config_handler import ConfigHandler
from dotpyle.services.config_parser import ConfigParser
from dotpyle.utils.get_source_and_link_path import get_source_and_link_path

# from dotpyle.decorators import init_handlers


handler = ConfigHandler()
parser = ConfigParser(config=handler.get_config())
repo = RepoHandler()


@click.command()
@click.option("--name", "-n", default="", help="program name")
@click.option("--profile", "-p", default="default", help="profile name")
@click.option(
    "--path", multiple=True, help="Program dotfiles paths starting from root path"
)
@click.option("--message", "-m", help="commit message")
# TODO: make path option name dependant
def commit(name, profile, path, message):
    all_keys = name == ""
    paths = [p for p in path]

    print(all_keys, paths)
    if all_keys:
        for name, profiles in parser.get_names_and_profiles():
            print(name, profile)
            print(parser.get_calculated_paths(name, profile))

    # repo.add(path='dotpyle.yml')
    # test()
