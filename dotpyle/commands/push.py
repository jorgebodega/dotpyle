import click

from dotpyle.decorators.pass_repo_handler import pass_repo_handler


@click.command()
@pass_repo_handler
def push(repo_handler):
    repo_handler.push()
