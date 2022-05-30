import click

from dotpyle.commands.init import init
from dotpyle.commands.add import add
from dotpyle.commands.edit import edit
from dotpyle.commands.ls import ls
from dotpyle.commands.link import link
from dotpyle.commands.unlink import unlink
from dotpyle.commands.commit import commit
from dotpyle.commands.push import push
from dotpyle.commands.pull import pull
from dotpyle.commands.switch import switch
from dotpyle.commands.shell import shell
from dotpyle.commands.run import run
from dotpyle.services.config_checker import ConfigChecker
from dotpyle.services.repo_handler import RepoHandler
from dotpyle.services.file_handler import FileHandler, LocalFileHandler
from dotpyle.services.logger import Logger
from dotpyle.utils import constants
from dotpyle.exceptions import DotpyleException
from dotpyle.services.config_manager import ConfigManager

CONTEXT = {"help_option_names": ["-h", "--help"]}


@click.group()
@click.version_option()
@click.option(
    "--verbose",
    "-v",
    "verbose",
    is_flag=True,
    help="Enable verbose mode",
)
@click.pass_context
def dotpyle(ctx=CONTEXT, verbose=False):
    """
    Manage your dotfiles, create multiple profiles for different programs,
    automate task with hooks, etc.
    """
    logger = Logger(verbose=verbose)
    try:
        handler = FileHandler(logger=logger)
        local_file_handler = LocalFileHandler(logger=logger)
    except:
        handler = None
        local_file_handler = None

    ctx.meta[constants.CONFIG_MANAGER_PROVIDER] = ConfigManager(
        file_handler=handler,
        local_file_handler=local_file_handler,
        logger=logger,
    )
    ctx.meta[constants.CONFIG_CHECKER_PROVIDER] = ConfigChecker()
    ctx.meta[constants.REPO_HANDLER_PROVIDER] = RepoHandler(logger=logger)
    ctx.meta[constants.LOGGER_PROVIDER] = logger
    ctx.meta[constants.FILE_HANDLER_PROVIDER] = handler
    ctx.meta[constants.LOCAL_FILE_HANDLER_PROVIDER] = local_file_handler


# Add commands to group
dotpyle.add_command(link)
dotpyle.add_command(unlink)
dotpyle.add_command(switch)

dotpyle.add_command(init)
dotpyle.add_command(add)
dotpyle.add_command(commit)
dotpyle.add_command(push)
dotpyle.add_command(pull)

dotpyle.add_command(edit)
dotpyle.add_command(ls)
dotpyle.add_command(shell)
dotpyle.add_command(run)


def main():
    try:
        dotpyle()
    except DotpyleException as e:
        logger = Logger(verbose=True)
        logger.failure(e)
        exit(e.code)


if __name__ == "__main__":
    main()
