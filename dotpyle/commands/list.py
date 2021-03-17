import click
from dotpyle.services.config_handler import ConfigHandler



@click.command()
@click.option('--name', '-n', default='all', help='program name')
@click.option('--profile', '-p', default='default', help='profile name')
def list(name, profile):

    cfh = ConfigHandler()
    print(name, profile)
    pass
