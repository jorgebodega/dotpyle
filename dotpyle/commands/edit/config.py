import click
from os import path
from shutil import copy2
from tempfile import gettempdir
from dotpyle.utils.path import get_configuration_path
from dotpyle.services.file_handler import FileHandler
from dotpyle.utils import constants
from dotpyle.decorators.pass_logger import pass_logger
from dotpyle.services.logger import Logger
from dotpyle.decorators.pass_config_manager import pass_config_manager
from dotpyle.services.config_manager import ConfigManager


@click.command()
@pass_config_manager
@pass_logger
def config(logger: Logger, manager: ConfigManager):
    """
    Open dotpyle.yml file in the default editor checking for changes and sync system
    """
    dotpyle_path = get_configuration_path()
    temp_config_file = path.join(
        gettempdir(), constants.DOTPYLE_CONFIG_FILE_NAME_TEMP
    )
    copy2(dotpyle_path, temp_config_file)

    # Open user default editor
    click.edit(filename=temp_config_file)

    config_file_handler = FileHandler(path=temp_config_file, logger=logger)

    manager.set_config_file_handler(config_file_handler)
    print("No errors found, your changes have been saved")
    copy2(temp_config_file, dotpyle_path)
