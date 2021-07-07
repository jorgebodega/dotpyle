"""config_handler.py """
import glob
import itertools
from os.path import join, isfile, isdir
from os import listdir
from yaml import safe_load, safe_dump
from dotpyle.errors.InvalidConfigFile import InvalidConfigFileError
from dotpyle.utils.path import get_configuration_path, get_dotfiles_path

import os
import shutil
import subprocess
from dotpyle.utils.path import (
    get_source_and_link_path,
    get_dotpyle_profile_path,
    get_dotpyle_name_path,
)
from dotpyle.services.config_checker import ConfigChecker
from dotpyle.exceptions import ConfigHandlerException


class ConfigHandler:
    """
    Methods to access and process Dotpyle configuration
    """

    def __init__(self, config):
        self._config = config

    @property
    def config(self):
        """
        :return:
            Internal configuration structure"""
        return self._config

    def get_dotfiles(self):
        """
        :return:
            Current dotfiles structure
        :raise ConfigHandlerException:
            If there is no dotfiles configured"""

        if "dotfiles" in self._config:
            return self._config["dotfiles"]
        raise ConfigHandlerException("Dotpyle database empty, no dotfiles found")

    def get_name(self, name):
        """
        :return:
            Dict with all profiles and configurations for a given name
        :raise ConfigHandlerException:
            If name does not exist on Dotpyle database"""

        dotfiles = self.get_dotfiles()
        if name in dotfiles:
            return dotfiles[name]
        raise ConfigHandlerException('Name "{}" does not exist'.format(name))

    def get_profile(self, profile, name):
        """
        :return:
            Dict with profile configurations for a given name
        :raise ConfigHandlerException:
            If profile does not exist on Dotpyle database"""

        key = self.get_name(name)
        if profile in key:
            return key[profile]
        raise ConfigHandlerException(
            'Profile "{}" for name "{}" does not exist'.format(profile, name)
        )

    def get_names_and_profiles(self):
        return [
            (name, [profile for profile in profiles])
            for name, profiles in self.get_dotfiles().items()
        ]

    def get_profile_paths(self, name, profile):
        return [source for source, _ in self.get_calculated_paths(name, profile)]

    def get_profiles_for_name(self, name: str):
        dotfiles = self.get_dotfiles()
        if name in dotfiles:
            return [profile for profile in dotfiles[name]]

    def get_calculated_paths(self, name, profile):
        # if name in self._config['dotfiles']:
        content = self._config["dotfiles"][name][profile]
        if not "root" in content:
            root = "~"  # TODO get $HOME
        else:
            root = content["root"]
        return [
            get_source_and_link_path(name, profile, root, path)
            for path in content["paths"]
        ]

    def check_config(self):
        return self.checker.check_config(self._config)

    def process_all_config(self, profile_name="default"):
        print("Parsing Dotpyle config")
        version = self._config["version"]
        if version != 1:
            raise ConfigHandlerException(
                "Version '{}' of dotfile.yml file is currently unsupported".format(
                    version
                )
            )
        for key in self._config["dotfiles"].keys():
            self.process_key(key, profile_name)

    def process_key(
        self,
        key_name,
        profile_name="default",
        process_pre=True,
        process_post=True,
    ):
        if profile_name in self._config["dotfiles"][key_name]:
            key = self._config["dotfiles"][key_name][profile_name]
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
                name=key_name,
                profile=profile_name,
                root=root,
                dotfile_path=path,
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

    def add_dotfile(self, name, profile, root, paths, pre_hooks, post_hooks):
        sources = []
        dotfiles = self.get_dotfiles()
        if name in dotfiles:
            existing_profiles = dotfiles[name]
            if profile in existing_profiles:
                # TODO throw error
                print(
                    "Profile {} for {} already exist on Dotpyle manager",
                    profile,
                    name,
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
            sources.append(source)

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

        # Return all the paths added to dotPyle repo
        return sources

    def uninstall_key_paths(self, name, profile, remove=False):
        dotfiles = self.get_dotfiles()
        if profile in dotfiles[name]:
            key = dotfiles[name][profile]
            paths = key["paths"]
            root = key["root"]
            for path in paths:
                source, link_name = get_source_and_link_path(name, profile, root, path)
                print("Removing {}".format(link_name))
                os.remove(link_name)

                # Before removing the file from dotPyle, copy where it should
                # be (in case remove flag is off)
                if not remove:
                    shutil.move(source, link_name)
                else:
                    os.remove(source)

            # Remove whole key when this profile is the last one
            if len(dotfiles[name]) == 1:
                del dotfiles[name]
                # Get key name path
                delete_path = get_dotpyle_name_path(name)

            # Remove only profile key
            else:
                del dotfiles[name][profile]
                # Get key+profile name path
                delete_path = get_dotpyle_profile_path(name, profile)
            # Warning: this will remove recursively the directories (empty or not)
            shutil.rmtree(delete_path)

            # TODO after remove, git add changes to make in consistent
        else:
            # TODO error
            print("Error: no key found")

    def change_profile(self, profile, name):
        pass
