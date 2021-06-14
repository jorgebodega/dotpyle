import click
from dotpyle.services.file_handler import FileHandler
from dotpyle.services.config_handler import ConfigHanlder
from dotpyle.utils.path import get_source_and_link_path

handler = FileHandler()
parser = ConfigHanlder(config=handler.get_config())


@click.command()
@click.argument("profile")
@click.argument("name", default="")
def checkout(profile, name):
    if name != "":
        parser.get_profile(profile, name)
    else:
        pass
