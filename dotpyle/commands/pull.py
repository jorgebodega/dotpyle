import click

from dotpyle.decorators.pass_repo_handler import pass_repo_handler


@click.command()
@pass_repo_handler
def pull(repo_handler):
    repo_handler.pull()
