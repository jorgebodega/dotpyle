import click
import dotpyle.utils.process as process
from dotpyle.utils.autocompletion import ScriptVarType
from dotpyle.decorators.pass_config_manager import pass_config_manager
from dotpyle.services.config_manager import ConfigManager

@click.command()
@click.help_option(help="Run a script managed by Dotpyle")
@click.argument("script", type=ScriptVarType())
@click.argument("arguments", nargs=-1)
@pass_config_manager
def run(manager: ConfigManager, script: str, arguments):
    """Run script"""

    script_path = manager.get_script_path(script)
    command = process.create_command(script_path, arguments)
    stdout = process.execute(command, True)
    # print(stdout)
