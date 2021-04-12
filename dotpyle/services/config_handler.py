from os.path import join, isfile, isdir
from os import listdir
import glob, itertools
from yaml import safe_load, safe_dump, load, dump
from dotpyle.utils import get_default_path
from sys import exit


class ConfigHandler:
    # TODO move this variables to global
    DOTPYLE_FILE = "dotpyle.yml"
    DOTFILES_FOLDER = "dotfiles"
    config = None

    def __init__(self, path=None):
        if not path:
            path = join(get_default_path(), self.DOTPYLE_FILE)

        if isfile(path):
            self.stream = open(path, "r+")
            self.config = self.read()

        else:
            exit("File {0} does not exist".format(path))

    def read(self):
        config = safe_load(self.stream)
        return config

    def save(self, config):
        self.stream.seek(0)
        self.stream.truncate()
        safe_dump(config, self.stream)

    def get_config(self):
        return self.config

    def set_config(self, new_config):
        # TODO maybe call check_config first?
        self.config = new_config

    def get_key_paths(self):
        dotfiles_path = join(get_default_path(), self.DOTFILES_FOLDER)
        return [
            join(dotfiles_path, key)
            for key in [
                f for f in listdir(dotfiles_path) if isdir(join(dotfiles_path, f))
            ]
        ]

    # TODO
    def get_profile_paths(self, key, profile):
        dotfiles_path = join(get_default_path(), self.DOTFILES_FOLDER)
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
