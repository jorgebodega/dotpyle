import os
from typing import Any
from rich.tree import Tree
from rich.text import Text
from dotpyle.utils import path
from dotpyle.objects.base import PathLike, ShellCommand
from dotpyle.objects.action import BaseAction, LinkAction, UnlinkAction, ScriptAction, RepoAction


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
        self._paths = paths
        self._root = root
        self._post = post
        self._pre = pre
        # Internals
        self._is_linked = False  # Set false by default (checked later)
        self._process_pre = False
        self._process_post = False
        self._track = track

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
                path.get_link_path(str(self._root), _path)
            )
            text_filename = Text(_path, "green")
            text_filename.stylize(f"link file://{_path}")
            text_filename += Text(" --> ", "blink yellow")
            text_filename += Text(link_path, "yellow")
            tree.add(Text("📄 ") + text_filename)
        return tree

    @property
    def profile_name(self) -> str:
        return self._profile_name

    @profile_name.setter
    def profile_name(self, profile_name) -> None:
        self._profile_name = profile_name

    @property
    def paths(self) -> list[str]:
        return self._paths

    @paths.setter
    def paths(self, paths: list[str]) -> None:
        self._paths = paths

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

    def _serialize(self) -> dict[str, Any]:
        serialized: dict[str, Any] = { "paths": self._paths }
        if self._root != '~':
            serialized["root"] = self._root
        if self._pre:
            serialized["pre"] = self._pre
        if self._post:
            serialized["post"] = self._post
        return serialized


    def _get_pending_actions(self) -> list[BaseAction]:
        pending_actions: list[BaseAction] = []
        for _path in self.paths:
            source, link = path.get_source_and_link_path(
                self._dotfile_name, self.profile_name, str(self._root), _path
            )
            path_linked = os.path.islink(link)
            path_correctly_linked = (
                os.readlink(link) == source if path_linked else False
            )
            if self.linked:
                if not path_linked or not path_correctly_linked:
                    pending_actions.append(LinkAction(source, link))
            else:
                if path_linked and path_correctly_linked:
                    pending_actions.append(UnlinkAction(link))

            if self._process_pre:
                pending_actions.append(ScriptAction(self._pre))
            if self._process_post:
                pending_actions.append(ScriptAction(self._post))

        print('track', self, self._dotfile_name, self._track)
        if self._track:
            pending_actions.append(RepoAction(self))

        return pending_actions


