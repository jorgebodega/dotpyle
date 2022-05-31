from typing import Any
from dotpyle.objects.base import DotpyleObject, Refreshed
from dotpyle.objects.action import BaseAction


class Path(DotpyleObject):
    __slots__ = ("_path",)

    def __init__(self, path: str, refreshed: Refreshed = Refreshed.QUERY):
        self._path = path
        self.refreshed = refreshed

    @property
    def path(self) -> str:
        return self._path

    @path.setter
    def path(self, path: str):
        self._path = path

    def serialize(
        self, check_refreshed: Refreshed = Refreshed.QUERY
    ) -> dict[str, Any]:
        return {}

    def get_pending_actions(
        self, check_refreshed: Refreshed = Refreshed.QUERY
    ) -> list[BaseAction]:
        return []
