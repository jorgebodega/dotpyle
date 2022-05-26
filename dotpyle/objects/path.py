class Path:
    __slots__ = (
        "_updated",
        "_path",
    )

    def __init__(self, path: str, updated: bool = False):
        self._path = path
        self._updated = updated

    @property
    def path(self) -> str:
        return self._path

    @path.setter
    def path(self, path: str):
        self._path = path

    @property
    def updated(self) -> bool:
        return self._updated

    @updated.setter
    def updated(self, updated: bool):
        self._updated = updated
