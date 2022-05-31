from enum import Enum
from typing import Any
from abc import ABC, abstractmethod
from dotpyle.objects.action import BaseAction


class Refreshed(Enum):
    QUERY = 0
    CONFIG = 1
    LOCAL = 2


class DotpyleObject(ABC):
    @property
    def track(self) -> bool:
        return self._track

    @track.setter
    def track(self, track: bool) -> None:
        self._track = track

    @property
    def refreshed(self) -> Refreshed:
        return self._refreshed

    @refreshed.setter
    def refreshed(self, refreshed: Refreshed) -> None:
        self._refreshed = refreshed

    @abstractmethod
    def serialize(
        self, check_refreshed: Refreshed = Refreshed.QUERY
    ) -> dict[str, Any]:
        """Return a dict representation of the whole object"""
        ...

    @abstractmethod
    def get_pending_actions(
        self, check_refreshed: Refreshed = Refreshed.QUERY
    ) -> list[BaseAction]:
        ...
