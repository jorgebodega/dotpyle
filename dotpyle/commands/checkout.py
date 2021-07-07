import click
from dotpyle.services.file_handler import FileHandler
from dotpyle.services.config_handler import ConfigHandler
from dotpyle.utils.path import get_source_and_link_path


@click.command()
@click.argument("profile")
@click.argument("name", default="")
def checkout(profile, name):
    handler = FileHandler()
    parser = ConfigHandler(config=handler.get_config())
    if name != "":
        parser.get_profile(profile, name)
    else:
        pass
