from click import get_app_dir
from os import getenv, path

APP_NAME = "dotpyle"


def get_default_path():
    """
    We need to know where to store information. If XDG_CONFIG_HOME is defined, use it.
    In any other case, it will use click.get_app_dir as default.

    Ref: https://click.palletsprojects.com/en/7.x/api/#click.get_app_dir
    """

    # TODO On MacOs get_app_dir return ~/Applications/Application Support/{NAME}
    default_config_path = getenv("XDG_CONFIG_HOME", "~/.config")

    return path.expanduser("{0}/{1}".format(default_config_path, APP_NAME))
