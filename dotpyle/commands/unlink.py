import click
from dotpyle.services.file_handler import FileHandler, LocalFileHandler
from dotpyle.services.config_handler import ConfigHandler
from dotpyle.services.print_handler import error, ok
from dotpyle.decorators.pass_config_handler import pass_config_handler
from dotpyle.decorators.pass_local_handler import pass_local_handler
from dotpyle.decorators.pass_logger import pass_logger


@click.command()
@click.argument("name")
@click.option("--profile", "-p", default="default", help="profile name")
@pass_local_handler
@pass_config_handler
@pass_logger
def unlink(logger, config_handler, local_handler, name, profile):
    """
    Unlink dotfiles for a program (and profile). Dotfiles will not
    be removed from Dotpyle repository
    """

    if not local_handler.is_profile_installed(name, profile):
        error("Profile {} is not installed for {}".format(profile, name))
        return

    config_handler.uninstall_paths(name, profile)
    local_handler.uninstall_profile(name)
    local_handler.save(local_handler.config)
    ok("{} dotfiles uninstalled".format(name))  # TODO: Refactor logger service
