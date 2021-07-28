import glob
import itertools
from os.path import join, isfile, isdir
from os import listdir
import sys
from yaml import safe_load, safe_dump
from dotpyle.utils.path import (
    get_configuration_path,
    get_local_configuration_path,
    get_dotfiles_path,
    get_script_path,
)
from shutil import copy2
from dotpyle.utils import constants


class BasicFileHandler:
    def __init__(self, file_path, template_path):
        if not file_path:
            print("TODO error, exit")

        if not isfile(file_path):
            print(
                "File {0} does not exist. Creating from template...".format(file_path)
            )
            copy2(template_path, file_path)

        self.stream = open(file_path, "r+")
        self._config = self.read()

    def read(self):
        return safe_load(self.stream)

    def save(self, config=None):
        self.stream.seek(0)
        self.stream.truncate()
        if not config:
            config = self.config
        safe_dump(config, self.stream)

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, new_config):
        # TODO maybe call check_config first?
        self._config = new_config


class FileHandler(BasicFileHandler):
    def __init__(self, path=None):
        if not path:
            path = get_configuration_path()
        BasicFileHandler.__init__(self, path, constants.CONFIG_TEMPLATE_PATH)

    # TODO deprecated
    def get_key_paths(self):
        dotfiles_path = join(get_dotfiles_path())
        return [
            join(dotfiles_path, key)
            for key in [
                f for f in listdir(dotfiles_path) if isdir(join(dotfiles_path, f))
            ]
        ]

    def get_profile_paths(self, key, profile):
        dotfiles_path = join(get_dotfiles_path())
        for key in [f for f in listdir(dotfiles_path) if isdir(join(dotfiles_path, f))]:
            key_path = join(dotfiles_path, key)
            for prof in [f for f in listdir(key_path) if isdir(join(key_path, f))]:
                prof_path = join(key_path, prof)
                return list(
                    itertools.chain(
                        glob.iglob(join(prof_path, "**")),
                        glob.iglob(join(prof_path, ".**")),
                    )
                )


class LocalFileHandler(BasicFileHandler):
    def __init__(self, path=None):
        if not path:
            path = get_local_configuration_path()
        BasicFileHandler.__init__(self, path, constants.CONFIG_LOCAL_TEMPLATE_PATH)

    def install_profile(self, name, profile):
        self.config["installed"][name] = profile

    def uninstall_profile(self, name):
        del self.config["installed"][name]

    def is_profile_installed(self, name, value):
        return (
            name in self.config["installed"] and self.config["installed"][name] == value
        )


class ScriptFileHandler(BasicFileHandler):
    def __init__(self, script_name):
        script_path = get_script_path(script_name)
        BasicFileHandler.__init__(self, script_path, constants.SCRIPT_TEMPLATE_PATH)
