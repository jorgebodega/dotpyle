from click.shell_completion import CompletionItem
from click import ParamType
from dotpyle.exceptions import FileHandlerException
from dotpyle.services.config_manager import ConfigManager
from dotpyle.services.file_handler import FileHandler, LocalFileHandler
import os

# This is awful: should be done with inyection
from dotpyle.services.logger import Logger


logger = Logger(verbose=False)
try:
    manager = ConfigManager(
        file_handler=FileHandler(logger),
        local_file_handler=LocalFileHandler(logger),
        logger=logger,
    )
    dotfile_names = manager.get_dotfile_names()
    profile_names = manager.get_profile_names()
    script_names = manager.get_script_names()

except FileHandlerException as e:
    dotfile_names = []
    profile_names = []
    script_names = []


class DotfileNamesVarType(ParamType):
    def shell_complete(self, ctx, param, incomplete):
        items = [(name, "") for name in dotfile_names]
        for value, help in items:
            if incomplete in value or incomplete in help:
                yield (CompletionItem(value, help=help))


# TODO: get profiles given name (previous argument)
# TODO https://stackoverflow.com/a/58617108/10474917
class ProfileVarType(ParamType):
    def shell_complete(self, ctx, param, incomplete):
        items = [(name, "") for name in profile_names]
        for value, help in items:
            if incomplete in value or incomplete in help:
                yield (CompletionItem(value, help=help))


class ScriptVarType(ParamType):
    def shell_complete(self, ctx, param, incomplete):
        items = [(name, "") for name in script_names]
        # For now, there will be no help
        for value, help in items:
            if incomplete in value or incomplete in help:
                yield (CompletionItem(value, help=help))


class EnvVarType(ParamType):
    def shell_complete(self, ctx, param, incomplete):
        return [
            CompletionItem(name)
            for name in os.environ
            if name.startswith(incomplete)
        ]


# No parece posible autocompletar con paths empezando en ~ o en / o en ../
# FIXME
# type=click.Path(exists=True, resolve_path=True, allow_dash=True)
class PathVarType(ParamType):
    def shell_complete(self, ctx, param, incomplete):
        import os

        return [CompletionItem(path) for path in os.listdir("/")]
