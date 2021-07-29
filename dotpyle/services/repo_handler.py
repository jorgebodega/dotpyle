from os import path
from typing import Callable, Optional
from git import Repo, PathLike
from shutil import rmtree
from dotpyle.utils.path import get_configuration_path, get_default_path


class RepoHandler:
    def __init__(self, local_path: PathLike = get_default_path()):
        self.local_path = local_path
        if path.exists(local_path):
            self.repo = Repo(local_path)

    def clone(
        self,
        remote_url: PathLike,
        force: bool = False,
        progress_listener: Optional[Callable] = None,
        branch_name: str = None,
    ) -> Repo:
        if path.exists(self.local_path):
            if force:
                rmtree(self.local_path)
            else:
                raise FileExistsError(
                    "Default path already exists. Please use --force to override."
                )

        self.repo = Repo.clone_from(
            url=remote_url,
            to_path=self.local_path,
            progress=progress_listener,
            branch=branch_name,
        )
        return self.repo

    def add(self, paths, config_file_changed=False):
        # self.repo.git.add(all=True)
        self.repo.git.add(paths)
        if config_file_changed:
            self.repo.git.add(get_configuration_path())

    def commit(self, message):
        self.repo.index.commit(message)

    def push(self):
        self.repo.git.push()

    def pull(self):
        self.repo.git.pull()
