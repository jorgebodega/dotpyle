import click
from dotpyle.decorators.pass_config_handler import pass_config_handler
from dotpyle.decorators.pass_local_handler import pass_local_handler
from dotpyle.decorators.pass_logger import pass_logger
from dotpyle.utils.autocompletion import DotfileNamesVarType, ProfileVarType
from dotpyle.decorators.pass_config_handler import pass_config_handler


@click.command()
@click.argument("name", type=DotfileNamesVarType())
@click.argument("profile", type=ProfileVarType())
@pass_local_handler
@pass_config_handler
@pass_logger
def switch(logger, config_handler, local_handler, name, profile):
    """Change profile for a given program"""

    if local_handler.is_profile_installed(name, profile):
        logger.failure(
            "Profile {} already installed for {}".format(profile, name)
        )
        return
    old_profile = local_handler.get_installed_profile(name)

    if profile not in config_handler.get_profiles_for_name(name):
        # TODO: suggest a profile creation with current changes
        logger.failure(
            "'{}' profile does not exist for '{}'".format(profile, name)
        )
        return

    config_handler.uninstall_paths(name, profile)
    config_handler.install_key(
        key_name=name,
        profile_name=profile,
        process_pre=False,
        process_post=False,
    )
    local_handler.install_profile(name, profile)
    local_handler.save()
    logger.success(
        "Switched profile '{}' to '{}' for {} ".format(
            old_profile, profile, name
        )
    )
