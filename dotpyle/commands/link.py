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
@click.option("--no-pre", is_flag=True, help="Don't execute pre hooks")
@click.option("--no-post", is_flag=True, help="Don't execute post hooks")
@click.option(
    "--no-hooks", is_flag=True, help="Don't execute pre and post hooks"
)
@pass_local_handler
@pass_config_handler
@pass_logger
def link(
    logger: Logger,
    config_handler: ConfigHandler,
    local_handler: LocalFileHandler,
    name: str,
    profile: str,
    no_pre: bool,
    no_post: bool,
    no_hooks: bool,
):
    """Link dotfiles for a given program and profile (and optionally execute hooks)"""

    if local_handler.is_profile_installed(name, profile):
        logger.failure(
            "Profile {} already installed for {}".format(profile, name)
        )
        return

    process_pre = not (no_pre or no_hooks)
    process_post = not (no_post or no_hooks)
    config_handler.install_key(
        key_name=name,
        profile_name=profile,
        process_pre=process_pre,
        process_post=process_post,
    )
    local_handler.install_profile(name, profile)
    local_handler.save(local_handler.config)
    logger.success("{} dotfiles installed".format(name))
