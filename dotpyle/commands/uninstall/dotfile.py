import click
from dotpyle.services.file_handler import FileHandler
from dotpyle.services.config_handler import ConfigHandler
from dotpyle.utils.path import get_source_and_link_path


@click.command()
@click.argument("name")
@click.option("--profile", "-p", default="default", help="profile name")
@click.option(
    "--remove-from-system",
    "-R",
    is_flag=True,
    help="remove files from system (not only from dotPyle)",
)
def dotfile(name, profile, remove_from_system):
    handler = FileHandler()
    parser = ConfigHandler(config=handler.get_config())

    parser.uninstall_key_paths(name, profile, remove_from_system)
    handler.save(parser.config)
