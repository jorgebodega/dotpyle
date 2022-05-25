import os
from typing import Any
from rich.tree import Tree
from rich.text import Text
from dotpyle.utils import path
from dotpyle.objects.base import PathLike, ShellCommand
from dotpyle.objects.path import Path
from dotpyle.objects.action import (
    BaseAction,
    LinkAction,
    UnlinkAction,
    ScriptAction,
    RepoAction,
    MoveAction,
    RemoveAction,
)


class Profile(object):
    __slots__ = (
        "_dotfile_name",
        "_profile_name",
        "_paths",
        "_post",
        "_pre",
        "_root",
        "_is_linked",
        "_process_pre",
        "_process_post",
        "_track",
        "_updated",
        "_updated_dict",
    )

    def __init__(
        self,
        dotfile_name: str,
        profile_name: str,
        paths: list[str],
        root: PathLike = "~",
        pre: list[ShellCommand] = [],
        post: list[ShellCommand] = [],
        track: bool = False,
    ) -> None:
        self._dotfile_name = dotfile_name
        self._profile_name = profile_name
        self._paths = [Path(path) for path in paths]
        self._root = root
        self._post = post
        self._pre = pre
        # Internals
        self._is_linked = False  # Set false by default (checked later)
        self._process_pre = False
        self._process_post = False
        self._track = track
        self._updated = False
        self._updated_dict = {}

    def __str__(self) -> str:
        return self._profile_name

    def _get_tree(self) -> Tree:
        tree = Tree(
            "[bold blue]:open_file_folder: [link"
            f" file://{self._profile_name}]{self._profile_name}"
            f" {'[bold green][LINKED]' if self._is_linked else ''}"
        )
        for _path in self._paths:
            link_path = path.un_expanduser(
                path.get_link_path(str(self._root), _path.path)
            )
            text_filename = Text(_path.path, "green")
            text_filename.stylize(f"link file://{_path.path}")
            text_filename += Text(" --> ", "blink yellow")
            text_filename += Text(link_path, "yellow")
            tree.add(Text("📄 ") + text_filename)
        return tree

    @property
    def dotfile_name(self) -> str:
        return self._dotfile_name

    @property
    def profile_name(self) -> str:
        return self._profile_name

    @profile_name.setter
    def profile_name(self, profile_name) -> None:
        self._profile_name = profile_name

    @property
    def paths(self) -> list[Path]:
        return self._paths

    @paths.setter
    def paths(self, paths: list[str]) -> None:
        if not paths:
            return
        # Update paths
        for path in paths:
            found = False
            for _path in self._paths:
                if _path.path == path:
                    # Mark as updated the non altered paths
                    # Removed paths will not be updated and an action will be generated
                    _path.updated = True
                    found = True
            if not found:
                print("path not found", path)
                # Added paths will be created with updated flag enabled
                self._paths.append(Path(path, updated=True))

    @property
    def root(self) -> PathLike:
        return self._root

    @root.setter
    def root(self, root: str) -> None:
        if self._root != root:
            self._updated_dict["last_root"] = self._root
        self._root = root

    @property
    def linked(self) -> bool:
        return self._is_linked

    @linked.setter
    def linked(self, linked: bool) -> None:
        self._is_linked = linked

    @property
    def process_pre(self) -> bool:
        return self._process_pre

    @process_pre.setter
    def process_pre(self, process: bool) -> None:
        self._process_pre = process

    @property
    def process_post(self) -> bool:
        return self._process_post

    @process_post.setter
    def process_post(self, process: bool) -> None:
        self._process_post = process

    @property
    def track(self) -> bool:
        return self._track

    @track.setter
    def track(self, track: bool) -> None:
        self._track = track

    @property
    def updated(self) -> bool:
        return self._updated

    @updated.setter
    def updated(self, updated: bool) -> None:
        self._updated = updated

    def get_link_paths(self) -> list[str]:
        return [
            path.get_link_path(str(self._root), _path.path)
            for _path in self.paths
        ]

    def get_repo_paths(self) -> list[str]:
        return [
            path.get_repo_paths(
                self.dotfile_name, self.profile_name, _path.path
            )
            for _path in self.paths
        ]

    def _serialize(self, check_updated: bool) -> dict[str, Any]:
        serialized: dict[str, Any] = {
            "paths": [
                path.path
                for path in self._paths
                if (not check_updated or path.updated)
            ]
        }
        if self._root != "~":
            serialized["root"] = self._root
        if self._pre:
            serialized["pre"] = self._pre
        if self._post:
            serialized["post"] = self._post
        return serialized

    def _get_pending_actions(self, check_updated: bool) -> list[BaseAction]:
        pending_actions: list[BaseAction] = []

        for _path in self.paths:
            source, link = path.get_source_and_link_path(
                self._dotfile_name,
                self.profile_name,
                str(self._root),
                _path.path,
            )

            path_linked = os.path.islink(link)
            path_correctly_linked = (
                os.readlink(link) == source if path_linked else False
            )
            source_path_exist = os.path.exists(source)

            if check_updated:
                if not _path.updated:
                    pending_actions.append(RemoveAction(source))
                # Remove all links
                if "last_root" in self._updated_dict and self.linked:
                    _, last_link = path.get_source_and_link_path(
                        self._dotfile_name,
                        self.profile_name,
                        self._updated_dict["last_root"],
                        _path.path,
                    )
                    pending_actions.append(UnlinkAction(last_link))

            if self._track:
                pending_actions.append(MoveAction(link, source))
            # This allows to add new paths to dotpyle.yml and to be linked automatically
            elif not source_path_exist:
                pending_actions.append(MoveAction(link, source))
                # TODO: RepoAction maybe to add and commit the new added paths

            if self.linked:
                if not path_linked or not path_correctly_linked:
                    pending_actions.append(LinkAction(source, link))
            else:
                if path_linked and path_correctly_linked:
                    pending_actions.append(UnlinkAction(link))

        # Create actions only if there are any actions to be executed
        if self._process_pre and self._pre:
            pending_actions.append(ScriptAction(self._pre))
        if self._process_post and self._post:
            pending_actions.append(ScriptAction(self._post))

        if self._track:
            pending_actions.append(RepoAction(self))

        return pending_actions
