import click
from os import system, path
from shutil import copy2
from tempfile import gettempdir
from dotpyle.utils.path import get_configuration_path, get_dotpyle_readme_path
from dotpyle.services.config_handler import ConfigHandler
from dotpyle.services.file_handler import FileHandler
from dotpyle.services.repo_handler import RepoHandler
from dotpyle import constants


@click.group()
def edit():
    """ Manually edit Dotpyle internal files """
    pass


@edit.command()
def config():
    dotpyle_path = get_configuration_path()
    temp_config_file = path.join(gettempdir(), constants.DOTPYLE_CONFIG_FILE_NAME_TEMP)
    copy2(dotpyle_path, temp_config_file)

    # Open user default editor
    click.edit(filename=temp_config_file)

    handler = FileHandler(path=temp_config_file)
    parser = ConfigHandler(config=handler.get_config())

    errors = parser.check_config()
    if errors == {}:
        print("No errors found, your changes have been saved")
        copy2(temp_config_file, dotpyle_path)

    else:
        print("Errors have been found on {}:\n")
        for key, value in errors.items():
            get_error(key, value)


@edit.command()
def readme():
    readme_path = get_dotpyle_readme_path()

    if not path.exists(readme_path):
        # Geterate a README with default template
        copy2(constants.README_TEMPLATE_PATH, readme_path)

    # Open user default editor
    res = click.edit(filename=readme_path)

    repo = RepoHandler()
    repo.add(constants.README_NAME, config_file_changed=False)


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
