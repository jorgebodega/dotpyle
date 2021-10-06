from abc import ABC, abstractmethod
import os
from dotpyle.objects.base import PathLike, ShellCommand


class BaseAction(ABC):
    @abstractmethod
    def run(self) -> None:
        ...

    @abstractmethod
    def rollback(self) -> None:
        ...


class LinkAction(BaseAction):
    def __init__(self, source: PathLike, link_name: PathLike):
        self.source = source
        self.link_name = link_name

    def __str__(self) -> str:
        return "[Link action]: link {} to {}".format(
            self.source, self.link_name
        )

    def run(self):
        os.symlink(src=self.source, dst=self.link_name)
        print("Linking {} -> {}".format(self.source, self.link_name))

    def rollback(self):
        os.unlink(self.link_name)
        print("Rallback: Unking {}".format(self.link_name))


class UnlinkAction(BaseAction):
    def __init__(self, link_name: PathLike):
        self.link_name = link_name

    def __str__(self) -> str:
        return "[Unlink action]: unlink {}".format(self.link_name)

    def run(self):
        self.source = os.readlink(self.link_name)
        os.unlink(self.link_name)
        print("Unking {}".format(self.link_name))

    def rollback(self):
        os.symlink(src=self.source, dst=self.link_name)
        print("Rollback: Linking {} -> {}".format(self.source, self.link_name))


class ScriptAction(BaseAction):
    def __init__(self, commands: list[ShellCommand]):
        self.commands = commands

    def __str__(self) -> str:
        return "[Script action]: commands:\n {}".format(self.commands)

    def run(self):
        print("Execute...\n {}".format(self.commands))

    def rollback(self):
        pass



