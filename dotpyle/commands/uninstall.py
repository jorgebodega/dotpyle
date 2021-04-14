import click
from dotpyle.services.config_handler import ConfigHandler
from dotpyle.services.config_parser import ConfigParser
from dotpyle.utils.path import get_source_and_link_path


@click.group()
def uninstall():
    """
    Uninstall a dotfile, hook, etc (TBD)
    """
    pass


handler = ConfigHandler()
parser = ConfigParser(config=handler.get_config())


@uninstall.command()
@click.argument("name")
@click.option("--profile", "-p", default="default", help="profile name")
@click.option(
    "--remove-from-system",
    "-R",
    is_flag=True,
    help="remove files from system (not only from dotPyle)",
)
def dotfile(name, profile, remove_from_system):
    parser.uninstall_key_paths(name, profile, remove_from_system)
    handler.save(parser.get_config())
