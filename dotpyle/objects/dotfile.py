from typing import Any
from dotpyle.objects.base import DotpyleObject, Refreshed
from dotpyle.objects.profile import Profile
from dotpyle.objects.action import BaseAction
from dotpyle.exceptions import ConfigManagerException
from rich.tree import Tree


class Dotfile(DotpyleObject):
    __slots__ = (
        "_program_name",
        "_profiles",
    )

    def __init__(
        self,
        program_name: str,
        profiles: dict[str, Profile] = {},
    ):
        self._program_name = program_name
        self._profiles = profiles

    @property
    def program_name(self):
        return self._program_name

    @program_name.setter
    def program_name(self, program_name):
        self._program_name = program_name

    @property
    def linked_profile(self):
        for profile in self._profiles.values():
            if profile.linked:
                return profile
        # return self._linked_profile

    @linked_profile.setter
    def linked_profile(self, profile_name):
        current_linked_profile = self.linked_profile
        if current_linked_profile:
            current_linked_profile.linked = False

        if profile_name in self._profiles:
            profile = self._profiles[profile_name]
            profile.linked = True

    @property
    def profiles(self):
        return self._profiles

    @profiles.setter
    def profiles(self, profiles):
        self._profiles = profiles

    def get_profile_names(self) -> list[str]:
        return list(self.profiles.keys())

    def get_profile(self, profile_name: str) -> Profile:
        if profile_name in self._profiles:
            return self._profiles[profile_name]
        raise ConfigManagerException(
            'Profile "{}" for name "{}" does not exist'.format(
                profile_name, self._program_name
            )
        )

    def __repr__(self):
        return "{} -> {} ".format(self.program_name, *self._profiles.values())

    def __str__(self) -> str:
        return "Program: {}\nProfiles:\n{}\n".format(
            self._program_name, *self._profiles.values()
        )

    def query_profiles(
        self, profile_filter: str, only_linked: bool
    ) -> list[Profile]:
        matched = []
        for profile_name, profile_data in self.profiles.items():
            if (not profile_filter or profile_filter in profile_name) and (
                not only_linked or profile_data.linked
            ):
                matched.append(profile_data)
        return matched

    def get_tree(
        self, profile_filter: str = "", only_linked: bool = False
    ) -> Tree:
        tree = Tree(f"[bold magenta]:open_file_folder: {self._program_name}")
        # for profile in self._profiles.values():
        for profile in self.query_profiles(profile_filter, only_linked):
            tree.add(profile._get_tree())
        return tree

    def serialize(
        self, check_refreshed: Refreshed = Refreshed.QUERY
    ) -> dict[str, Any]:
        return {
            profile_name: profile_data.serialize(check_refreshed)
            for profile_name, profile_data in self._profiles.items()
        }

    def get_pending_actions(
        self, check_refreshed: Refreshed = Refreshed.QUERY
    ) -> list[BaseAction]:
        pending_actions = []
        # if self._new:
        # pending_actions.append(mathe)
        for profile in self.profiles.values():
            pending_actions.extend(profile.get_pending_actions(check_refreshed))
        return pending_actions

    def add_profile(self, profile: Profile):
        # TODO validate profile
        profile.track = True
        print(profile, profile.track)
        self._profiles[profile.profile_name] = profile
        return self
