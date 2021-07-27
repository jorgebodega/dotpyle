import click
from dotpyle.services.file_handler import FileHandler, LocalFileHandler
from dotpyle.services.config_handler import ConfigHandler
from dotpyle.utils.path import get_source_and_link_path
from dotpyle.services.print_handler import error, warning, ok
from dotpyle.utils.autocompletion import get_names, get_profiles


@click.command()
@click.argument("name", shell_complete=get_names)
@click.argument("profile", shell_complete=get_profiles)
def switch(name, profile):
    """Change profile for a given program"""

    handler = FileHandler()
    parser = ConfigHandler(config=handler.config)

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

