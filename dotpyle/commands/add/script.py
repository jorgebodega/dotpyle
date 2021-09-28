import click
from dotpyle.decorators.pass_config_handler import pass_config_handler
from dotpyle.decorators.pass_file_handler import pass_file_handler
from dotpyle.utils.autocompletion import PathVarType
from dotpyle.decorators.pass_repo_handler import pass_repo_handler


@click.command()
@click.help_option(help="Add/edit script in order to execute it later")
@click.argument("path", type=PathVarType())
@click.argument("name")
@pass_config_handler
@pass_file_handler
@pass_repo_handler
def script(repo_handler, file_handler, config_handler, path, name):
    """Add/edit script in order to execute it later"""
    added_path = config_handler.add_script(path, name)
    file_handler.save(config_handler.config)

    repo_handler.add(added_path, config_file_changed=True)
    commit_message = "[dotpyle]: added {} script".format(name)
    repo_handler.commit(commit_message)
