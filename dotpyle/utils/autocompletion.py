from click.shell_completion import CompletionItem

from dotpyle.services.file_handler import FileHandler, LocalFileHandler
from dotpyle.services.config_handler import ConfigHandler
import os
import sys


def get_names(ctx, param, incomplete):
    handler = FileHandler()
    parser = ConfigHandler(config=handler.config)
    name_profiles = parser.get_names()

    items = [(name, "") for name in name_profiles]
    out = []
    for value, help in items:
        if incomplete in value or incomplete in help:
            # yield value
            out.append(CompletionItem(value, help=help))

    return out


# TODO: get profiles given name (previous argument)
def get_profiles(ctx, param, incomplete):
    handler = FileHandler()
    parser = ConfigHandler(config=handler.config)
    # first, *middle, last = ctx.split()
    name_profiles = parser.get_name("vim")

    # cmd_line = (tok for tok in param + [incomplete])
    # last = [p for p in parm]
    # cmd_line = " ".join(last + [incomplete])

    # f = open("test.txt", "a")
    # commandLineArgsAsStr = str(sys.argv)
    # numArgs = len(sys.argv)
    # f.write(str(incomplete))
    # f.write(commandLineArgsAsStr)
    # f.write(str(numArgs))
    # # f.write(str(ctx.command))
    # # f.write(str(ctx.info_name))
    # # f.write(str(param))
    # f.write('\n')
    # f.close()
    items = [(name, "") for name in name_profiles]
    out = []
    for value, help in items:
        if incomplete in value or incomplete in help:
            out.append(CompletionItem(value, help=help))

    return out
