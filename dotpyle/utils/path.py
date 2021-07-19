from click import get_app_dir
from os import getenv, path
from dotpyle.utils import constants


def get_default_path():
    """
    We need to know where to store information. If XDG_CONFIG_HOME is defined, use it.
    In any other case, it will use click.get_app_dir as default.

    Ref: https://click.palletsprojects.com/en/7.x/api/#click.get_app_dir
    """

    # TODO On MacOs get_app_dir return ~/Applications/Application Support/{NAME}
    default_config_path = getenv("XDG_CONFIG_HOME", "~/.config")

    return path.expanduser("{0}/{1}".format(default_config_path, constants.APP_NAME))


def get_configuration_path():
    return path.join(get_default_path(), constants.DOTPYLE_CONFIG_FILE_NAME)


def get_dotfiles_path():
    return path.join(get_default_path(), constants.DOTFILES_FOLDER)


def get_dotpyle_name_path(name):
    return path.join(get_dotfiles_path(), name)


def get_dotpyle_profile_path(name, profile):
    return path.join(get_dotpyle_name_path(name), profile)


def get_source_and_link_path(name, profile, root, dotfile_path):
    """
    source: absoulte path for name+profile inside dotPyle repo
    link_name: absoulte path for name+profile on realy system
    """
    # source = "{0}/dotfiles/{1}/{2}/{3}".format(dotpyle_path, name, profile, path)
    source = path.join(get_dotpyle_profile_path(name, profile), dotfile_path)
    # link_name = path.expanduser(root + "/" + path)
    link_name = path.expanduser(path.join(root, dotfile_path))
    return source, link_name


def get_dotpyle_readme_path():
    return path.join(get_default_path(), constants.README_NAME)
