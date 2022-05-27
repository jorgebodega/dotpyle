import click
from dotpyle.utils.autocompletion import PathVarType
from dotpyle.services.config_manager import ConfigManager
from dotpyle.decorators.pass_config_manager import pass_config_manager
from dotpyle.objects.script import Script

@click.command()
@click.help_option(help="Add/edit script in order to execute it later")
@click.argument("path", type=PathVarType())
@click.argument("alias")
@pass_config_manager
def script(
    manager: ConfigManager,
    path: str,
    alias: str
):
    """Add/edit script in order to execute it later"""
    script = Script(alias = alias, filename=path)
    added_path = manager.set_script(script)

    # TODO: add action to add or commit script
    # repo_handler.add(added_path, config_file_changed=True)
    # commit_message = "[dotpyle]: added {} script".format(name)
    # repo_handler.commit(commit_message)
