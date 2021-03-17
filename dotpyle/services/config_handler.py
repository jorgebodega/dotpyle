import os
from yaml import safe_load, safe_dump, load, dump
from dotpyle.utils import get_default_path
from sys import exit


class ConfigHandler:
    DOTPYLE_FILE = "dotpyle.yml"
    config = None

    def __init__(self, path=None):
        if not path:
            path = get_default_path() + "/" + self.DOTPYLE_FILE

        if os.path.isfile(path):
            self.stream = open(path, "r+")
            self.config = self.read()

        else:
            exit('File {0} does not exist'.format(path))

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
