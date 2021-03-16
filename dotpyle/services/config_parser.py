from os import symlink
import cerberus
import subprocess
from dotpyle.utils import get_default_path

class ConfigParser:
    def __init__(self, config):
        self.schema = eval(open("dotpyle/services/schema.py", "r").read())
        self.config = config
        self.dotpyle_path = get_default_path()

    def check_config(self):
        validator = cerberus.Validator(self.schema)
        valid = validator.validate(self.config)
        # if not valid:
        # print (validator.errors)
        # for error in validator.errors:
        # print('error',error)

        return validator.errors

    def process_all_config(self, profile_name='default'):
        print("Parsing Dotpyle config")
        # config = self.read()
        version = self.config["version"]
        if version != 1:
            return False
        for key in self.config["dotfiles"].keys():
            self.process_key(key, profile_name)

    def process_key(self, key_name, profile_name='default'):
        if profile_name in self.config['dotfiles'][key_name]:
            key = self.config['dotfiles'][key_name][profile_name]
            # 1. Proces pre hooks
            self.process_key_hooks(key["pre"])
            # 2. Proces paths
            self.process_key_paths(key_name, profile_name, key["root"], key["paths"])
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

    def process_key_paths(self, key_name, profile_name, root, paths):

        for path in paths:
            """
                root: ~/.config/nvim,
                paths: [
                    "init.vim",
                ]

            """
            # ln -s ~/.config/dotpyle/dotfiles/<key_name>/<profile_name>/<path>  <root>/<key_name>/<path>
            #symlink('{0}/dotfiles/{1}/{2}/{3}'.format(self.dotpyle_path, key_name, profile_name, path), root + '/' + path)
            print('{0}/dotfiles/{1}/{2}/{3}'.format(self.dotpyle_path, key_name, profile_name, path))
            print('')
            print(root + '/' + path)
