import os
import git
from dotpyle.utils import get_default_path


class RepoHandler:
    DOTPYLE_FILE = "dotpyle.yml"

    def __init__(self):
        repo_dir = get_default_path()
        self.repo = git.Repo(path=repo_dir)

    # usage: git add [<options>] [--] <pathspec>...

    # -n, --dry-run         dry run
    # -v, --verbose         be verbose

    # -i, --interactive     interactive picking
    # -p, --patch           select hunks interactively
    # -e, --edit            edit current diff and apply
    # -f, --force           allow adding otherwise ignored files
    # -u, --update          update tracked files
    # --renormalize         renormalize EOL of tracked files (implies -u)
    # -N, --intent-to-add   record only the fact that the path will be added later
    # -A, --all             add changes from all tracked and untracked files
    # --ignore-removal      ignore paths removed in the working tree (same as --no-all)
    # --refresh             don't add, only refresh the index
    # --ignore-errors       just skip files which cannot be added because of errors
    # --ignore-missing      check if - even missing - files are ignored in dry run
    # --chmod (+|-)x        override the executable bit of the listed files
    # --pathspec-from-file <file>
    # read pathspec from file
    # --pathspec-file-nul   with --pathspec-from-file, pathspec elements are separated with NUL character
    def add(self, paths, config_file_changed=False):
        # self.repo.git.add(all=True)
        self.repo.git.add(paths)
        if config_file_changed:
            self.repo.git.add(get_default_path() + self.DOTPYLE_FILE)
        print("added", paths)

    def commit(self, message):
        self.repo.index.commit(message)
