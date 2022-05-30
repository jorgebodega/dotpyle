import click

from dotpyle.decorators.pass_config_manager import pass_config_manager
from dotpyle.decorators.pass_repo_handler import pass_repo_handler
from dotpyle.services.config_manager import ConfigManager
from dotpyle.services.repo_handler import RepoHandler


@click.command()
@click.option("--name", "-n", default="", help="program name")
@click.option("--profile", "-p", default="", help="profile name")
@click.option("--message", "-m", help="commit message")
@pass_config_manager
@pass_repo_handler
# TODO: make path option name dependant
def commit(
    repo_handler: RepoHandler,
    manager: ConfigManager,
    name: str,
    profile: str,
    message,
):

    if not message:
        print("TODO: open default editor")
        return

    # Add files based on parameters
    for dotfile in manager.query_dotfiles(name):
        profiles = dotfile.query_profiles(profile, only_linked=False)
        for _profile in profiles:
            for path in _profile.get_repo_paths():
                # TODO: only add files that have been edited
                repo_handler.add(paths=path)

    # Proceed with commit
    repo_handler.commit(message)
