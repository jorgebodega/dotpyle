import click

from dotpyle.commands.init import init
from dotpyle.commands.edit import edit
from dotpyle.commands.add import add
from dotpyle.commands.ls import ls
from dotpyle.commands.config import config
from dotpyle.commands.link import link
from dotpyle.commands.unlink import unlink
from dotpyle.commands.commit import commit
from dotpyle.commands.checkout import checkout
from dotpyle.commands.push import push
from dotpyle.commands.pull import pull
from dotpyle.commands.switch import switch
from dotpyle.commands.script import script
from dotpyle.commands.shell import shell

from dotpyle.services.config_checker import ConfigChecker
from dotpyle.services.repo_handler import RepoHandler
from dotpyle.services.file_handler import FileHandler
from dotpyle.services.config_handler import ConfigHandler

from dotpyle.utils import constants
from dotpyle.services.print_handler import error
from dotpyle.exceptions import DotpyleException


from dotpyle.decorators.pass_repo_handler import pass_repo_handler


@click.group()
@click.version_option()
@click.pass_context
def dotpyle(ctx=None):
    """
    Manage your dotfiles, create multiple profiles for different programs,
    automate task with hooks, etc.
    """
    handler = FileHandler()
    parser = ConfigHandler(config=handler.config)
    ctx.meta[constants.CONFIG_CHECKER_PROVIDER] = ConfigChecker()
    ctx.meta[constants.REPO_HANDLER_PROVIDER] = RepoHandler()
    ctx.meta[constants.CONFIG_HANDLER_PROVIDER] = parser


# Add commands to group
dotpyle.add_command(link)
dotpyle.add_command(unlink)
dotpyle.add_command(switch)

dotpyle.add_command(init)
dotpyle.add_command(add)
dotpyle.add_command(commit)
dotpyle.add_command(push)
dotpyle.add_command(pull)
dotpyle.add_command(checkout)

dotpyle.add_command(config)
dotpyle.add_command(edit)
dotpyle.add_command(ls)
dotpyle.add_command(shell)

dotpyle.add_command(script)


@dotpyle.command()
@pass_repo_handler
def test(repo_handler: RepoHandler):
    repo_handler.clone(
        remote_url="https://github.com/jorgebodega/Dotfiles.git",
    )


def main():
    try:
        dotpyle()
    except DotpyleException as e:
        error(e)
        exit(e.code)


if __name__ == "__main__":
    main()
