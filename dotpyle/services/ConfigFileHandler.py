from os import path, symlink
import subprocess
from yaml import safe_load, safe_dump, load, dump
from dotpyle.utils import get_default_path
import cerberus


class ConfigFileHandler:
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

    def check_config(self, config_file=config):
        schema = eval(open("dotpyle/services/schema.py", "r").read())

        validator = cerberus.Validator(schema)
        valid = validator.validate(config_file)
        # if not valid:
        # print (validator.errors)
        # for error in validator.errors:
        # print('error',error)

        return validator.errors

    def process_all_config(self, config_file=config):
        print("Parsing Dotpyle config")
        # config = self.read()
        version = config_file["version"]
        if version != 1:
            return False
        for key in config_file["dotfiles"]:
            self.process_key(key)

    def process_key(self, key):
        # 1. Proces pre hooks
        self.process_key_hooks(key["pre"])
        # 2. Proces paths
        self.process_key_paths(root=key["root"], paths=key["paths"])
        # 3. Proces posts hooks
        self.process_key_hooks(key["post"])

    def process_key_hooks(self, hooks):
        print("Processing hooks")
        for hook in hooks:
            print("Executing hook", hook)
            # Avoid use of array with command name + pararms
            result = subprocess.run(
                "%s" % hook, capture_output=True, check=True, shell=True
            )
            result.check_returncode()  # Raise an exception if the command execution fails

    def process_key_paths(self, root, paths):
        for path in paths:
            symlink(path[0], path[1])
            pass
