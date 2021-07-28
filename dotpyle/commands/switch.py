import click
from dotpyle.services.file_handler import LocalFileHandler
from dotpyle.services.print_handler import error, ok
from dotpyle.utils.autocompletion import get_names, get_profiles
from dotpyle.decorators.pass_config_handler import pass_config_handler


@click.command()
@pass_config_handler
@click.argument("name", shell_complete=get_names)
@click.argument("profile", shell_complete=get_profiles)
def switch(parser, name, profile):
    """Change profile for a given program"""

    local_handler = LocalFileHandler()
    if local_handler.is_profile_installed(name, profile):
        error("Profile {} already installed for {}".format(profile, name))
        return

    parser.uninstall_paths(name, profile)

    parser.install_key(
        key_name=name,
        profile_name=profile,
        process_pre=False,
        process_post=False,
    )
    local_handler.install_profile(name, profile)
    local_handler.save()
    ok("{} dotfiles installed".format(name))
