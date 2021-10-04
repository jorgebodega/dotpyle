import os
from typing import Union, Any
from dotpyle.utils import path
from dotpyle.services.file_handler import FileHandler, LocalFileHandler
from dotpyle.services.logger import Logger
from dotpyle.exceptions import ConfigHandlerException

from rich.tree import Tree
from rich.text import Text

PathLike = Union[str, os.PathLike]
ShellCommand = str


class Profile(object):
    __slots__ = (
        "_dotfile_name",
        "_profile_name",
        "_paths",
        "_post",
        "_pre",
        "_root",
        "_is_linked",
    )

    def __init__(
        self,
        dotfile_name: str,
        profile_name: str,
        paths: list[str],
        root: PathLike = "~",
        pre: list[ShellCommand] = [],
        post: list[ShellCommand] = [],
    ):
        self._dotfile_name = dotfile_name
        self._profile_name = profile_name
        self._paths = paths
        self._root = root
        self._post = post
        self._pre = pre
        self._is_linked = False  # Set false by default (checked later)

    def __str__(self) -> str:
        return "\t\tPaths: {}\n\t-Root: {} TODO".format(self._paths, self._root)

    def _get_tree(self) -> Tree:
        tree = Tree(f"[bold blue]:open_file_folder: [link file://{self._profile_name}]{self._profile_name}")
        for _path in self._paths:
            link_path = path.un_expanduser(path.get_link_path(self._root, _path))
            text_filename = Text(_path, "green")
            text_filename.stylize(f"link file://{_path}")
            text_filename += Text(" --> ", "blink yellow")
            text_filename += Text(link_path, "yellow")
            tree.add(Text("📄 ") + text_filename)
        return tree

    @property
    def profile_name(self):
        return self._profile_name

    @profile_name.setter
    def profile_name(self, profile_name):
        self._profile_name = profile_name

    @property
    def paths(self) -> list[str]:
        return self._paths

    @paths.setter
    def paths(self, paths: list[str]) -> None:
        self._paths = paths

    @property
    def linked(self) -> bool:
        return self._is_linked

    @linked.setter
    def linked(self, linked: bool):
        self._is_linked = linked

    def _serialize(self):
        return {
            "paths": self._paths,
            "root": self._root,
            "pre": self._pre,
            "post": self._post,
        }

class Script(object):
    """Script class to manage all relation with the capacity of Dotpyle to
    store, track and execute scripts"""

    __slots__ = ("_alias", "_filename")

    def __init__(self, alias: str, filename: str) -> None:
        """Initialize script object to be managed by Dotpyle"""
        self._alias = alias
        self._filename = filename

    @property
    def alias(self) -> str:
        return self._alias

    @alias.setter
    def alias(self, alias):
        self._alias = alias

    @property
    def filename(self) -> str:
        return self._filename

    @filename.setter
    def filename(self, filename):
        self._filename = filename

    def get_path(self) -> PathLike:
        """:return: filename full path"""
        return path.get_script_path(self._filename)

    def __str__(self) -> str:
        return "Script: {} located on {}".format(self._alias, self.get_path())

    def _serialize(self):
        return self._filename
        # return {self._alias: self._filename}


class Dotfile(object):
    __slots__ = (
        "_program_name",
        "_profiles",
        "_linked_profile",
    )

    def __init__(
        self,
        program_name: str,
        profiles: dict[str, Profile],
    ):
        self._program_name = program_name
        self._profiles = profiles
        self._linked_profile = None

    @property
    def program_name(self):
        return self._program_name

    @program_name.setter
    def program_name(self, program_name):
        self._program_name = program_name

    @property
    def linked_profile(self):
        return self._linked_profile

    @linked_profile.setter
    def linked_profile(self, profile_name):
        if profile_name in self._profiles:
            profile = self._profiles[profile_name]
            # Set linked profile to internal profile
            profile.linked = True
            self._linked_profile = profile

    def __str__(self) -> str:
        return "Program: {}\nProfiles:\n{}\nIntalled profile: {}".format(
            self._program_name, *self._profiles.values(), self._linked_profile
        )

    def _get_tree(self) -> Tree:
        tree = Tree(
            # f"[bold magenta]:open_file_folder: [link file://{self._program_name}]{self._program_name}"
            f"[bold magenta]:open_file_folder: {self._program_name} {'[bold green][LINKED]' if self._linked_profile else ''}"
        )
        for profile in self._profiles.values():
            tree.add(profile._get_tree())
        return tree

    def _serialize(self):
        return {
            self._program_name: {
                profile_name: profile_data._serialize()
                for profile_name, profile_data in self._profiles.items()
            }
        }


class ConfigManager:
    """
    Methods to access and process Dotpyle configuration
    """

    __slots__ = (
        "_dotfiles",
        "_scripts",
        "_config_file_handler",
        "_local_file_handler",
        "_logger",
        "_version",
    )

    def __init__(self, logger: Logger, config_path=None) -> None:
        self._logger = logger
        # self.checker = ConfigChecker()
        self._config_file_handler = FileHandler(logger=logger, path=config_path)
        self._local_file_handler = LocalFileHandler(
            logger=logger, path=config_path
        )
        self._scripts: dict[str, Script] = {}
        self._dotfiles: dict[str, Dotfile] = {}
        self._load_config()

    def _load_config(self) -> None:
        """Read dotpyle.yml config file and creates a OOP mapping of all fields"""
        self._load_general_config()

        """Read dotpyle.local.yml config file and set which dotfiles are linked"""
        self._load_local_config()

        self._logger.log(*self._dotfiles.values())
        for dotfile in self._dotfiles.values():
            self._logger.log(dotfile._get_tree())

    def _load_general_config(self) -> None:
        """Read dotpyle.yml config file and creates a OOP mapping of all fields"""
        config_dict = self._config_file_handler.config
        try:
            self._version = config_dict["version"]
            if self._version != 0:
                raise ConfigHandlerException(
                    "Version '{}' of dotfile.yml file is currently unsupported"
                    .format(self._version)
                )
            if "scripts" in config_dict:
                self._scripts = {
                    alias: Script(alias, filename)
                    for alias, filename in config_dict["scripts"].items()
                }
                self._logger.log(*self._scripts.values())

            if "dotfiles" in config_dict:
                dotfiles_dict = {}
                raw_dotfiles = config_dict["dotfiles"].items()
                for (dotfile_name, raw_profiles) in raw_dotfiles:
                    profiles_dict = {}
                    for profile_name, profile_data in raw_profiles.items():
                        profile = Profile(
                            dotfile_name=dotfile_name,
                            profile_name=profile_name,
                            paths=profile_data.get("paths", []),
                            root=profile_data.get("root", None),
                            pre=profile_data.get("pre", []),
                            post=profile_data.get("post", []),
                        )
                        profiles_dict[profile_name] = profile
                    dotfiles_dict[dotfile_name] = Dotfile(
                        program_name=dotfile_name,
                        profiles=profiles_dict,
                    )

                self._dotfiles = dotfiles_dict

        except KeyError as e:
            print(e)  # TODO

    def _load_local_config(self) -> None:
        """Read dotpyle.local.yml config file and enrich current dotfiles with proper information"""
        local_dict = self._local_file_handler.config
        version = local_dict.get("version", None)
        if version != 0:
            raise ConfigHandlerException(
                "Version '{}' of dotfile.local.yml file is currently unsupported"
                .format(version)
            )
        installed_profiles = local_dict.get("installed", {})
        for dotfile, profile in installed_profiles.items():
            self.get_dotfile(dotfile).linked_profile = profile

    def _get_linked_dotfiles(self) -> list[Dotfile]:
        """Auxiliar mothod to obtain current linked profiles"""
        linked_dotfiles = []
        for dotfile in self._dotfiles.values():
            if dotfile.linked_profile:
                linked_dotfiles.append(dotfile.linked_profile)
        return linked_dotfiles

    def _get_linked_profiles(self) -> dict[str,str]:
        """Auxiliar mothod to obtain current linked profiles"""
        linked_profiles = {}
        for dotfile in self._dotfiles.values():
            if dotfile.linked_profile:
                linked_profiles[dotfile.program_name] = dotfile.linked_profile.profile_name
        return linked_profiles

    def _serialize_general_config(self) -> dict[str, Any]:
        """Convert all objects back to dict format (dotpyle.yml)"""
        serialized_config = {
            "dotfiles": {
                dotfile_name: dotfile_data._serialize()
                for dotfile_name, dotfile_data in self._dotfiles.items()
            },
            "scripts": {
                script_name: script_data._serialize()
                for script_name, script_data in self._scripts.items()
            },
            "version": self._version,  # here could be updated to newer supported versions (future)
            "settings": self._config_file_handler.config["settings"],
        }
        self._logger.log(serialized_config)
        return serialized_config

    def _serialize_local_config(self) -> dict[str, Any]:
        """Convert all objects back to dict format (dotpyle.local.yml)"""
        serialized_local_config = {
            "installed": self._get_linked_profiles(),
            "version": self._version,  # here could be updated to newer supported versions (future)
        }
        self._logger.log(serialized_local_config)
        return serialized_local_config

    def _save_config(self) -> None:
        self._config_file_handler.save(self._serialize_general_config())
        self._local_file_handler.save(self._serialize_local_config())

    def get_dotfile(self, program_name: str) -> Dotfile:
        if program_name in self._dotfiles:
            return self._dotfiles[program_name]
        raise ConfigHandlerException('Dotfile "{}" does not exist'.format(program_name))

    def edit_dotfile(self, program_name: str):
        pass

    def remove_dotfile(self):
        pass
