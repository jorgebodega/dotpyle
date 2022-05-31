from dotpyle.objects.base import Refreshed
from dotpyle.services.logger import Logger
from dotpyle.services.file_handler import FileHandler, LocalFileHandler
from dotpyle.exceptions import ConfigManagerException
from dotpyle.objects.script import Script
from dotpyle.objects.dotfile import Dotfile
from dotpyle.objects.action import BaseAction
from dotpyle.objects.profile import Profile
from typing import Any


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
        "_abort",
        "_refreshed",
        "_cli_mode",
        "_initialized",
    )

    def __init__(
        self,
        file_handler: FileHandler | None,
        local_file_handler: LocalFileHandler | None,
        logger: Logger,
    ) -> None:
        self._logger = logger
        # self.checker = ConfigChecker()
        self._config_file_handler = file_handler
        self._local_file_handler = local_file_handler
        self._scripts: dict[str, Script] = {}
        self._dotfiles: dict[str, Dotfile] = {}
        self._abort = False
        self._refreshed = Refreshed.QUERY
        self._cli_mode = False

        if file_handler and local_file_handler:
            self._load_config()
            self._initialized = True
        else:
            self._initialized = False

    def __del__(self):
        # Only perform actions in editing mode
        if (
            self._refreshed != Refreshed.QUERY or self._cli_mode
        ) and not self._abort:
            try:
                # First save config file
                self._save_config(refreshed=self._refreshed)
                self._logger.log("Config file saved successfully")
                self._run_pending_actions(self._refreshed)
                # TODO rollback config file storage
                self._logger.log("Pending actions done")
            except:
                self._rollback_actions()
                self._logger.failure("Error, rolled back")

    def _load_config(self) -> None:
        """Read dotpyle.yml config file and creates a OOP mapping of all fields"""
        self._load_general_config()

        """Read dotpyle.local.yml config file and set which dotfiles are linked"""
        self._load_local_config()

    def _load_general_config(self) -> None:
        """Read dotpyle.yml config file and creates a OOP mapping of all fields"""
        config_dict = self._config_file_handler.config
        try:
            self._version = config_dict["version"]
            if self._version != 0:
                raise ConfigManagerException(
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
                            root=profile_data.get("root", "~"),
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

    def _update_general_config(self, new_config: FileHandler) -> None:
        """TODO dotpyle.yml config file and creates a OOP mapping of all fields"""
        self._config_file_handler = new_config
        config_dict = self._config_file_handler.config

        self._refreshed = (
            Refreshed.CONFIG
        )  # Ensure all operations will work as updated

        try:
            self._version = config_dict["version"]
            if self._version != 0:
                raise ConfigManagerException(
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
                raw_dotfiles = config_dict["dotfiles"].items()
                for (dotfile_name, raw_profiles) in raw_dotfiles:
                    # Mark profile as updated
                    dotfile = self.get_dotfile(dotfile_name)
                    dotfile.refreshed = Refreshed.CONFIG

                    for profile_name, profile_data in raw_profiles.items():
                        # Mark profile as updated
                        profile = dotfile.get_profile(profile_name)
                        profile.refreshed = Refreshed.CONFIG
                        profile.paths = profile_data.get("paths", [])
                        root = profile_data.get("root", "~")
                        profile.root = root
                        # TODO
                        # profile.pre = profile_data.get("pre", []),
                        # profile.post = profile_data.get("post", []),

        except KeyError as e:
            print(e)  # TODO

    def _load_local_config(self) -> None:
        """Read dotpyle.local.yml config file and enrich current dotfiles with proper information"""
        local_dict = self._local_file_handler.config
        version = local_dict.get("version", None)
        if version != 0:
            raise ConfigManagerException(
                "Version '{}' of dotfile.local.yml file is currently"
                " unsupported".format(version)
            )
        installed_profiles = local_dict.get("installed", {})

        for dotfile, profile in installed_profiles.items():
            # self.get_dotfile(dotfile).get_profile(profile).linked = True
            self.get_dotfile(dotfile).linked_profile = profile

    def _update_local_config(self, new_local_config: LocalFileHandler) -> None:
        """Read dotpyle.local.yml config file and enrich current dotfiles with proper information"""

        self._local_file_handler = new_local_config
        local_dict = self._local_file_handler.config

        self._refreshed = (
            Refreshed.LOCAL
        )  # Ensure all operations will work as updated

        version = local_dict.get("version", None)
        if version != 0:
            raise ConfigManagerException(
                "Version '{}' of dotfile.local.yml file is currently"
                " unsupported".format(version)
            )
        installed_profiles = local_dict.get("installed", {})

        for dotfile_name, profile_name in installed_profiles.items():
            # self.get_dotfile(dotfile).get_profile(profile).linked = True
            dotfile = self.get_dotfile(dotfile_name)
            dotfile.linked_profile = profile_name
            profile = dotfile.get_profile(profile_name)
            profile.refreshed = Refreshed.LOCAL
            # TODO find another way to set as refreshed all paths while updating only local config
            for path in profile.paths:
                path.refreshed = Refreshed.LOCAL

    def _get_linked_dotfiles(self) -> list[Dotfile]:
        """Auxiliar mothod to obtain current linked profiles"""
        linked_dotfiles = []
        for dotfile in self._dotfiles.values():
            if dotfile.linked_profile:
                linked_dotfiles.append(dotfile.linked_profile)
        return linked_dotfiles

    def _get_linked_profiles(self) -> dict[str, str]:
        """Auxiliar mothod to obtain current linked profiles"""
        linked_profiles = {}
        for dotfile in self._dotfiles.values():
            if dotfile.linked_profile:
                linked_profiles[
                    dotfile.program_name
                ] = dotfile.linked_profile.profile_name
        return linked_profiles

    def _serialize_general_config(
        self, check_updated: Refreshed
    ) -> dict[str, Any]:
        """Convert all objects back to dict format (dotpyle.yml)"""
        serialized_config = {
            "dotfiles": {
                dotfile_name: dotfile_data.serialize(check_updated)
                for dotfile_name, dotfile_data in self._dotfiles.items()
            },
            "scripts": {
                script_name: script_data.serialize()
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

    def _save_config(self, refreshed: Refreshed) -> None:
        self._config_file_handler.save(
            self._serialize_general_config(refreshed)
        )
        self._local_file_handler.save(self._serialize_local_config())

    def _get_pending_actions(
        self, check_updated: Refreshed
    ) -> list[BaseAction]:
        pending_actions = []
        for dotfile in self._dotfiles.values():
            pending_actions.extend(dotfile.get_pending_actions(check_updated))

        # Sort pending actions by priority
        pending_actions = sorted(
            pending_actions, key=lambda x: x.priority, reverse=True
        )

        return pending_actions

    def _rollback_actions(
        self,
        actions: list[BaseAction] = [],
        check_updated: Refreshed = Refreshed.QUERY,
    ):
        if actions == []:
            actions = self._get_pending_actions(check_updated=check_updated)
        # Iterate over all executed actions backwards, rollbacking them
        for action in actions[::-1]:
            action.rollback()
        pass

    def _run_pending_actions(
        self, check_updated: Refreshed = Refreshed.QUERY
    ) -> None:
        run_actions: list[BaseAction] = []
        try:
            for action in self._get_pending_actions(check_updated):
                self._logger.log(action)
                run_actions.append(action)
                action.run()
        except:
            # Rollback executed actions
            self._rollback_actions(run_actions, check_updated)

    def query_dotfiles(self, program_name: str) -> list[Dotfile]:
        match = []
        if program_name:
            match = [
                dotfile_data
                for dotfile_name, dotfile_data in self._dotfiles.items()
                if dotfile_name == program_name
            ]
        else:
            match.extend(self._dotfiles.values())
        return match

    def get_dotfile(self, program_name: str) -> Dotfile:
        if program_name in self._dotfiles:
            return self._dotfiles[program_name]
        raise ConfigManagerException(
            'Dotfile "{}" does not exist'.format(program_name)
        )

    def get_script_path(self, script_name) -> str:
        """
        :return:
        :raise ConfigHandlerException:
            If name does not exist on Dotpyle database"""
        if script_name in self._scripts:
            return self._scripts[script_name].get_path()
        raise ConfigManagerException(
            'Script "{}" does not exist'.format(script_name)
        )

    def set_dotfile(self, dotfile: Dotfile) -> None:
        self._cli_mode = True
        self._dotfiles[dotfile.program_name] = dotfile

    def set_script(self, script: Script) -> None:
        pass

    def edit_dotfile(self, program_name: str):
        pass

    def remove_dotfile(self):
        pass

    def set_config_file_handler(self, config_file_handler: FileHandler):
        try:
            self._update_general_config(new_config=config_file_handler)
        except ConfigManagerException as e:
            self._abort = True
            raise e

    def set_local_file_handler(self, local_file_handler: LocalFileHandler):
        try:
            self._update_local_config(local_file_handler)
        except ConfigManagerException as e:
            self._abort = True
            raise e

    def get_dotfile_names(self) -> list[str]:
        """
        :return:
            List with all program names managed by Dotpyle
        """
        return [name for name in self._dotfiles.keys()]

    def get_profile_names(self) -> list[str]:
        """
        :return:
            List with all profiles managed by Dotpyle
        """
        profiles = set()
        for dotfile in self._dotfiles.values():
            for profile_name in dotfile.profiles.keys():
                profiles.add(profile_name)
        return list(profiles)

    def get_script_names(self) -> list[str]:
        """
        :return:
            List with all profiles managed by Dotpyle
        """
        return [script_name for script_name in self._scripts.keys()]

    def initilize_repo(self):
        if not self._initialized:
            pass
