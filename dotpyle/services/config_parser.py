import os
import shutil
import cerberus
import subprocess
from dotpyle.utils import get_source_and_link_path


class ConfigParser:
    def __init__(self, config):
        self.schema = eval(open("dotpyle/services/schema.py", "r").read())
        self.config = config

    def check_config(self):
        validator = cerberus.Validator(self.schema)
        valid = validator.validate(self.config)
        # if not valid:
        # print (validator.errors)
        # for error in validator.errors:
        # print('error',error)

        return validator.errors

    def process_all_config(self, profile_name="default"):
        print("Parsing Dotpyle config")
        # config = self.read()
        version = self.config["version"]
        if version != 1:
            return False
        for key in self.config["dotfiles"].keys():
            self.process_key(key, profile_name)

    def process_key(
        self, key_name, profile_name="default", process_pre=True, process_post=True
    ):
        if profile_name in self.config["dotfiles"][key_name]:
            key = self.config["dotfiles"][key_name][profile_name]
            # 1. Proces pre hooks
            if process_pre and "pre" in key:
                self.process_key_hooks(key["pre"])
            # 2. Proces paths
            self.process_key_paths(key_name, profile_name, key["root"], key["paths"])
            # 3. Proces posts hooks
            if process_post and "post" in key:
                self.process_key_hooks(key["post"])

    def process_key_hooks(self, hooks):
        print("Processing hooks")
        for hook in hooks:
            print("Executing hook", hook)
            # Avoid use of array with command name + pararms
            result = subprocess.run(
                "%s" % hook, capture_output=False, check=True, shell=True
            )
            # print(result.stdout)
            result.check_returncode()  # Raise an exception if the command execution fails

    def process_key_paths(self, key_name, profile_name, root, paths):

        for path in paths:
            """
            root: ~/.config/nvim,
            paths: [
                "init.vim",
            ]

            """
            source, link_name = get_source_and_link_path(
                name=key_name, profile=profile_name, root=root, path=path
            )
            # source = '{0}/dotfiles/{1}/{2}/{3}'.format(self.dotpyle_path, key_name, profile_name, path)
            # link_name = root + "/" + path
            # ln -s ~/.config/dotpyle/dotfiles/<key_name>/<profile_name>/<path>  <root>/<key_name>/<path>
            print(">>> ln -s {0} {1}".format(source, link_name))
            if os.path.isfile(link_name):
                # TODO throw error or give user possibility to replace
                print("Error >> {0} already exist".format(link_name))
            else:
                os.symlink(source, link_name)

    def get_dotfiles(self):
        return self.config["dotfiles"]

    def get_names_and_profiles(self):
        # return [(name, profile) for profile in seq_x for name, profiles in self.get_dotfiles().items()]
        # return [(name, profiles) for name, profiles in self.get_dotfiles().items()]
        return [
            (name, [profile for profile in profiles])
            for name, profiles in self.get_dotfiles().items()
        ]

        # for name, profiles in self.get_dotfiles.items():
        # for profile in profiles:
        # pass

    def get_calculated_paths(self, name, profile):
        # if name in self.config['dotfiles']:
        content = self.config["dotfiles"][name][profile]
        if not "root" in content:
            root = "~"  # TODO get $HOME
        else:
            root = content["root"]
        return [
            get_source_and_link_path(name, profile, root, path)
            for path in content["paths"]
        ]

    def add_dotfile(self, name, profile, root, paths, pre_hooks, post_hooks):
        dotfiles = self.get_dotfiles()
        if name in dotfiles:
            existing_profiles = dotfiles[name]
            if profile in existing_profiles:
                # TODO throw error
                print(
                    "Profile {} for {} already exist on Dotpyle manager", profile, name
                )
        else:
            dotfiles[name] = {}

        new_profile = {
            "root": root,
            "paths": paths,
        }

        if pre_hooks:
            new_profile["pre"] = pre_hooks
        if post_hooks:
            new_profile["post"] = post_hooks

        dotfiles[name][profile] = new_profile

        for path in paths:
            # Get source path (destination path on dotpyle repo) and current file path
            source, link_name = get_source_and_link_path(name, profile, root, path)

            profile_directory_path = os.path.dirname(source)
            # Create (recursively) profile and key name directory on dotpyle/dotfiles path
            os.makedirs(profile_directory_path, exist_ok=True)
            try:
                # Move existing path to dotpyle repo
                # shutil.move does not work with symlinks
                shutil.copy(link_name, source)
                os.remove(link_name)
                # Symlink path in order to start tracking changes
                os.symlink(source, link_name)
            except shutil.SameFileError as exc:
                # TODO
                print("Error >> This file is already been managed by Dotpyle")

        # TODO move away from here please
        from dotpyle.services.config_handler import ConfigHandler

        handler = ConfigHandler()
        handler.save(self.config)
