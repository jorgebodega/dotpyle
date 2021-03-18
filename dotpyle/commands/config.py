import click

from dotpyle.utils.get_default_path import get_default_path
from dotpyle.services.config_parser import ConfigParser
from dotpyle.services.config_handler import ConfigHandler


@click.group()
def config():
    pass


@config.command()
@click.option(
    "--path", "-p", default=get_default_path(), help="path for alternative dotpyle.yml"
)
def check(path):
    path_file = path + "/dotpyle.yml"
    print("Checking", path_file, "...")
    config = ConfigHandler().get_config()
    parser = ConfigParser(config)

    errors = parser.check_config()
    if errors == {}:
        print("No errors found, your config is OK")
    else:
        print("Following erros have been found on {}:\n".format(path_file))
        for key, value in errors.items():
            get_error(key, value)


def get_error(key, value):
    if type(value) == list:
        for elem in value:
            get_error(key, elem)
    elif type(value) == dict:
        for k, v in value.items():
            get_error(key + " -> " + k, v)
    else:
        print(" - {}: '{}'".format(key, value))
