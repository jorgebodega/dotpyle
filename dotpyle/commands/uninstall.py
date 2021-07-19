import click
from dotpyle.services.file_handler import FileHandler, LocalFileHandler
from dotpyle.services.config_handler import ConfigHandler
from dotpyle.utils.path import get_source_and_link_path
from dotpyle.services.print_handler import error, warning, ok


@click.command()
@click.argument("name")
@click.option("--profile", "-p", default="default", help="profile name")
@click.option(
    "--remove-from-system",
    "-R",
    is_flag=True,
    help="remove files from system (not only from dotpyle)",
)
def uninstall(name, profile, remove_from_system):
    """
    Uninstall a dotfile, hook, etc (TBD)
    """
    local_handler = LocalFileHandler()

    if not local_handler.is_profile_installed(name, profile):
        error("Profile {} is not installed for {}".format(profile, name))
        return

    handler = FileHandler()
    parser = ConfigHandler(config=handler.config)

    parser.uninstall_paths(name, profile, remove_from_system)
    local_handler.uninstall_profile(name)
    local_handler.save()
    ok("{} dotfiles uninstalled".format(name))
