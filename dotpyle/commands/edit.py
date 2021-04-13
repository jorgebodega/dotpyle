import click
from os import system
from dotpyle.utils.path import get_configuration_path


@click.command()
def edit():
    dotpyle_path = get_configuration_path()
    system("$EDITOR {}".format(dotpyle_path))
