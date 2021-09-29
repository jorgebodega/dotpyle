import click
from dotpyle.utils.autocompletion import DotfileNamesVarType, ProfileVarType
from dotpyle.decorators.pass_config_handler import pass_config_handler
from dotpyle.decorators.pass_local_handler import pass_local_handler
from dotpyle.decorators.pass_logger import pass_logger
from dotpyle.decorators.pass_config_handler import pass_config_handler
from dotpyle.decorators.pass_repo_handler import pass_repo_handler
from dotpyle.services.logger import Logger
from dotpyle.services.config_handler import ConfigHandler
from dotpyle.services.file_handler import LocalFileHandler
from dotpyle.services.repo_handler import RepoHandler


@click.command()
@click.argument("name", type=DotfileNamesVarType())
@click.argument("profile", type=ProfileVarType())
@click.option(
    "--create-profile",
    is_flag=True,
    help=(
        "Force profile creation when given profile does not exist for given"
        " program"
    ),
)
@pass_local_handler
@pass_config_handler
@pass_repo_handler
@pass_logger
def switch(
    logger: Logger,
    repo_handler: RepoHandler,
    config_handler: ConfigHandler,
    local_handler: LocalFileHandler,
    name: str,
    profile: str,
    create_profile,
):
    """Change profile for a given program"""

    if local_handler.is_profile_installed(name, profile):
        logger.failure(
            "Profile {} already installed for {}".format(profile, name)
        )
        return
    old_profile = local_handler.get_installed_profile(name)

    if profile not in config_handler.get_profiles_for_name(name):
        if not create_profile:
            logger.failure(
                "'{}' profile does not exist for '{}', use --create-profile to"
                " create a new profile with current changes".format(
                    profile, name
                )
            )
            return

        current_profile_path = config_handler.get_profile_paths(
            name, old_profile
        )
        print(current_profile_path)
        if repo_handler.check_changes(current_profile_path):
            logger.failure("TODO: git changes")
            return

    config_handler.uninstall_paths(name, profile)
    config_handler.install_key(
        key_name=name,
        profile_name=profile,
        process_pre=False,
        process_post=False,
    )
    local_handler.install_profile(name, profile)
    local_handler.save(local_handler.config)
    logger.success(
        "Switched profile '{}' to '{}' for {} ".format(
            old_profile, profile, name
        )
    )
