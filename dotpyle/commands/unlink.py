import click
from dotpyle.services.file_handler import FileHandler, LocalFileHandler
from dotpyle.services.config_handler import ConfigHandler
from dotpyle.services.print_handler import error, ok


@click.command()
@click.argument("name")
@click.option("--profile", "-p", default="default", help="profile name")
def unlink(name, profile):
    """
    Unlink dotfiles for a program (and profile). Dotfiles will not
    be removed from Dotpyle repository
    """
    local_handler = LocalFileHandler()

    if not local_handler.is_profile_installed(name, profile):
        error("Profile {} is not installed for {}".format(profile, name))
        return

    handler = FileHandler()
    parser = ConfigHandler(config=handler.config)

    parser.uninstall_paths(name, profile)
    local_handler.uninstall_profile(name)
    local_handler.save()
    ok("{} dotfiles uninstalled".format(name))  # TODO: Refactor logger service
