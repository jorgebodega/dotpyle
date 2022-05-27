from typing import Any
from dotpyle.objects.action import BaseAction, MoveAction
from dotpyle.objects.action import RemoveAction
from dotpyle.objects.base import DotpyleObject
from dotpyle.objects.common import PathLike
from dotpyle.utils import path


class Script(DotpyleObject):
    """Script class to manage all relation with the capacity of Dotpyle to
    store, track and execute scripts"""

    __slots__ = ("_alias", "_filename")

    def __init__(self, alias: str, filename: str) -> None:
        """Initialize script object to be managed by Dotpyle"""
        self._alias = alias
        self._filename = filename
        self._track = False
        self._refreshed = False

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

    def get_path(self) -> str:
        """:return: filename full path"""
        return path.get_script_path(self._filename)

    def __str__(self) -> str:
        return "Script: {} located on {}\n".format(self._alias, self.get_path())

    def serialize(self, check_refreshed: bool = False) -> dict[str, Any]:
        if check_refreshed and not self.refreshed:
            return {}
        return self._filename


    def get_pending_actions(self, check_refreshed: bool = False) -> list[BaseAction]:
        pending_actions: list[BaseAction] = []
         
        if self.track:
            # TODO add to repo
            # pending_actions.append(RepoAction(self))
            pending_actions.append(MoveAction(source_path = self.filename, dest_path=self.get_path()))

        if check_refreshed and not self.refreshed:
                pending_actions.append(RemoveAction(self.get_path()))

        return pending_actions


