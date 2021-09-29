import click
from dotpyle.decorators.pass_config_handler import pass_config_handler
from dotpyle.decorators.pass_local_handler import pass_local_handler
from dotpyle.decorators.pass_logger import pass_logger
from dotpyle.utils.autocompletion import ProfileVarType, DotfileNamesVarType
from dotpyle.services.logger import Logger
from dotpyle.services.config_handler import ConfigHandler
from dotpyle.services.file_handler import LocalFileHandler


@click.command()
@click.argument("name", type=DotfileNamesVarType())
@click.option(
    "--profile",
    "-p",
    default="default",
    help="profile name",
    type=ProfileVarType(),
)
@pass_local_handler
@pass_config_handler
@pass_logger
def unlink(
    logger: Logger,
    config_handler: ConfigHandler,
    local_handler: LocalFileHandler,
    name: str,
    profile: str,
):
    """
    Unlink dotfiles for a program (and profile). Dotfiles will not
    be removed from Dotpyle repository
    """

    if not local_handler.is_profile_installed(name, profile):
        logger.failure(
            "Profile {} is not installed for {}".format(profile, name)
        )
        return

    config_handler.uninstall_paths(name, profile)
    local_handler.uninstall_profile(name)
    local_handler.save(local_handler.config)
    logger.success("{} dotfiles uninstalled".format(name))
