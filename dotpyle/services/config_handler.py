from os import path, symlink
from yaml import safe_load, safe_dump, load, dump
from dotpyle.utils import get_default_path


class ConfigHandler:
    DOTPYLE_FILE = "dotpyle.yml"
    config = None
    route = None

    def __init__(self, path=None):
        if path:
            self.stream = open(path, "r+")
        else:
            self.route = get_default_path()
            self.stream = open(self.route + "/" + self.DOTPYLE_FILE, "r+")

        self.config = self.read()

    def read(self):
        config = safe_load(self.stream)
        return config

    def save(self, config):
        self.stream.seek(0)
        self.stream.truncate()
        safe_dump(config, self.stream)


