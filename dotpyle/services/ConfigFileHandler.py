from os import path, symlink
import subprocess
from yaml import safe_load, safe_dump, load, dump
from dotpyle.utils import get_default_path


class ConfigFileHandler:
    DOTPYLE_FILE = "dotpyle.yml"
    stream = None
    route = None

    def __init__(self):
        self.route = get_default_path()
        self.stream = open(self.route + '/' + self.DOTPYLE_FILE, 'r+')

    def read(self):
        config = safe_load(self.stream)
        return config

    def save(self, config):
        self.stream.seek(0)
        self.stream.truncate()
        safe_dump(config, self.stream)

    def process_all_config(self):
        print('Parsing Dotpyle config')
        config = self.read()
        for key in config:
            self.process_key(key)
        print(config)

    def process_key(self, key):
        # 1. Proces pre hooks
        self.process_key_hooks(key['pre'])
        # 2. Proces paths
        self.process_key_paths(key['paths'])
        # 3. Proces posts hooks
        self.process_key_hooks(key['post'])

    def process_key_hooks(self, hooks):
        print('Processing hooks')
        for hook in hooks:
            print('Executing hook', hook)
            # Avoid use of array with command name + pararms
            result = subprocess.run('%s' % hook , capture_output=True, check=True, shell=True)
            result.check_returncode() # Raise an exception if the command execution fails


    def process_key_paths(self, paths):
        for path in paths:
            symlink(path[0], path[1])
            pass

