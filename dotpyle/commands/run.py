import click
from dotpyle.decorators.pass_config_handler import pass_config_handler
import subprocess
import dotpyle.utils.process as process
from dotpyle.utils.autocompletion import ScriptVarType


@click.command()
@click.help_option(help="Run a script managed by Dotpyle")
@click.argument("script", type=ScriptVarType())
@click.argument("arguments", nargs=-1)
@pass_config_handler
def run(config_handler, script, arguments):
    """Run script"""

    script_path = config_handler.get_script_path(script)
    command = process.create_command(script_path, arguments)
    stdout = process.execute(command, True)
    print(stdout)
