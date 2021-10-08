from abc import ABC, abstractmethod
import os
from dotpyle.services.repo_handler import RepoHandler
from dotpyle.decorators.pass_repo_handler import pass_repo_handler
from dotpyle.objects.base import PathLike, ShellCommand
# from dotpyle.objects.profile import Profile


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


class RepoAction(BaseAction):
    def __init__(self, profile): # TODO cannot type Profile (circular dependency)
        self.profile = profile

    def __str__(self) -> str:
        return "[Repo action]: "

    # @pass_repo_handler
    def run(self): #, repo_handler: RepoHandler):
        # commit_message = "[dotpyle]: added {} on {} profile on {} program".format(
            # added_paths, profile, name
        # )
        # repo_handler.add(added_paths, config_file_changed=True)
        # repo_handler.commit(commit_message)
        # print('repo_handler', repo_handler)
        print("Added paths: {}, of profile {} on program {}".format(self.profile.paths, self.profile.profile_name, self.profile._dotfile_name ))

    def rollback(self):
        pass
