import click

from dotpyle.utils.path import get_default_path, get_configuration_path
from dotpyle.services.config_handler import ConfigHandler
from dotpyle.services.file_handler import FileHandler
from dotpyle.services.print_handler import print


@click.group()
def config():
    pass


@config.command()
@click.option(
    "--path",
    "-p",
    default=get_default_path(),
    help="path for alternative dotpyle.yml",
)
def check(path):
    path_file = get_configuration_path()
    print("Checking {}...".format(path_file))
    config = FileHandler().config
    parser = ConfigHandler(config)

    errors = parser.check_config()
    if errors == {}:
        print("No errors found, your config is OK")
    else:
        print("Following erros have been found on {}:\n".format(path_file))
        print(errors)
        for key, value in errors.items():
            get_error(key, value)


# TODO: move this to ConfigParser and create exceptions
def get_error(key, value):
    if type(value) == list:
        for elem in value:
            get_error(key, elem)
    elif type(value) == dict:
        for k, v in value.items():
            get_error(key + " -> " + k, v)
    else:
        print(" - {}: '{}'".format(key, value))
