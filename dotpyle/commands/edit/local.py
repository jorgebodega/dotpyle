import click
from os import path
from shutil import copy2
from tempfile import gettempdir
from dotpyle.utils.path import get_local_configuration_path
from dotpyle.services.file_handler import LocalFileHandler
from dotpyle.services.config_manager import ConfigManager
from dotpyle.utils import constants
from dotpyle.decorators.pass_logger import pass_logger
from dotpyle.services.logger import Logger
from dotpyle.decorators.pass_config_manager import pass_config_manager
from dotpyle.services.config_manager import ConfigManager


@click.command()
@pass_config_manager
@pass_logger
def local(logger: Logger, manager: ConfigManager):
    """
    Open dotpyle.local.yml file in the default editor checking for changes and sync system
    """
    dotpyle_local_path = get_local_configuration_path()
    temp_local_config_file = path.join(
        gettempdir(), constants.DOTPYLE_LOCAL_CONFIG_FILE_NAME_TEMP
    )
    copy2(dotpyle_local_path, temp_local_config_file)

    # Open user default editor
    click.edit(filename=temp_local_config_file)

    local_file_handler = LocalFileHandler(
        path=temp_local_config_file, logger=logger
    )
    manager.set_local_file_handler(local_file_handler)

    # If an error occurs (profile or dotfile dont exist, will raise an exception)
    print("No errors found, your changes have been saved")
    copy2(temp_local_config_file, dotpyle_local_path)
