import click

from dotpyle.commands.init import init
from dotpyle.commands.edit import edit
from dotpyle.commands.help import help
from dotpyle.commands.add import add
from dotpyle.commands.list import list
from dotpyle.commands.config import config
from dotpyle.commands.link import link
from dotpyle.commands.unlink import unlink
from dotpyle.commands.commit import commit
from dotpyle.commands.checkout import checkout
from dotpyle.commands.push import push
from dotpyle.commands.pull import pull

from dotpyle.services.print_handler import error
from dotpyle.exceptions import DotpyleException


@click.group()
def dotpyle():
    """ Needed to create different commands with different options """
    pass


# Add commands to group
dotpyle.add_command(init)
dotpyle.add_command(add)
dotpyle.add_command(link)
dotpyle.add_command(unlink)

dotpyle.add_command(commit)
dotpyle.add_command(push)
dotpyle.add_command(pull)
dotpyle.add_command(checkout)

dotpyle.add_command(config)
dotpyle.add_command(edit)
dotpyle.add_command(list)
dotpyle.add_command(help)


def main():
    try:
        dotpyle()
    except DotpyleException as e:
        error(e)
        exit(e.code)


if __name__ == "__main__":
    main()
