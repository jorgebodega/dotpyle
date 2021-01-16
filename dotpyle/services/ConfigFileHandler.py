from os import path
from yaml import safe_load, safe_dump, load, dump
from dotpyle.utils import get_default_path


class ConfigFileHandler:
    DOTPYLE_FILE = "dotpyle.yml"
    stream = None
    route = None

    def __init__(self):
        # route = get_default_path()
        self.route = '/home/perseo/Documents/codes/dotpyle/'
        self.stream = open(self.route + '/' + self.DOTPYLE_FILE, 'r+')

    def read(self):
        config = safe_load(self.stream)
        return config

    def save(self, config):
        self.stream.seek(0)
        self.stream.truncate()
        safe_dump(config, self.stream)

