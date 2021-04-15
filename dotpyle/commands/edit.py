import click
from os import system, path
from shutil import copy2
from tempfile import gettempdir
from dotpyle.utils.path import get_configuration_path
from dotpyle.services.config_parser import ConfigParser
from dotpyle.services.config_handler import ConfigHandler
from dotpyle import constants


@click.command()
def edit():
    dotpyle_path = get_configuration_path()
    temp_config_file = path.join(gettempdir(), constants.DOTPYLE_CONFIG_FILE_NAME_TEMP)
    copy2(dotpyle_path, temp_config_file)

    # Open user default editor
    click.edit(filename=temp_config_file)

    handler = ConfigHandler(path=temp_config_file)
    parser = ConfigParser(config=handler.get_config())

    errors = parser.check_config()
    if errors == {}:
        print("No errors found, your changes have been saved")
        copy2(temp_config_file, dotpyle_path)

    else:
        print("Erros have been found on {}:\n")
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
