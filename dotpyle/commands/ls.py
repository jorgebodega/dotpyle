import click
from dotpyle.services.file_handler import FileHandler
from dotpyle.services.config_handler import ConfigHandler
from dotpyle.utils.path import get_source_and_link_path, un_expanduser
import os
import pathlib
import sys

import rich
from rich.filesize import decimal
from rich.markup import escape
from rich.text import Text
from rich.tree import Tree

from dotpyle.utils.autocompletion import get_names, get_profiles

# TODO: flag all
@click.command()
@click.argument("name", required=False, shell_complete=get_names)
@click.option(
    "--profile", "-p", help="profile name", shell_complete=get_profiles
)
@click.option(
    "--all", "-a", is_flag=True, help="list all dotfiles (linked or not)"
)
def ls(name, profile, all):

    config = FileHandler().config
    parser = ConfigHandler(config)

    dotfiles = parser.get_dotfiles()

    tree = Tree(
        "🌲 [b green]dotfiles",
        highlight=True,
        # f"[bold magenta]:open_file_folder:dotfiles",
        guide_style="bold bright_blue",
    )
    # Filtering by name
    if name:
        if name in dotfiles:
            profiles = dotfiles[name]
            if profile:
                if profile in profiles:
                    print_dotfiles(
                        tree, name, profile, profiles[profile], parser
                    )
                else:
                    print(
                        "Profile {} in {} does not exist".format(profile, name)
                    )

            # Get all profiles for given name
            else:
                for profile_name, content in profiles.items():
                    print_dotfiles(tree, name, profile_name, content, parser)

    # Get all names
    else:
        # Filtering only by profiles
        if profile:
            for program_name, profiles in dotfiles.items():
                if profile in profiles:
                    print_dotfiles(
                        tree, program_name, profile, profiles[profile], parser
                    )

        else:
            for program_name, profiles in dotfiles.items():
                for profile_name, content in profiles.items():
                    print_dotfiles(
                        tree, program_name, profile_name, content, parser
                    )

    rich.print(tree)


def print_dotfiles(tree, name, profile, content, parser):
    tree = tree.add(
        f"[bold magenta]:open_file_folder: [link file://{name}]{name}"
    ).add(f"[bold blue]:open_file_folder: [link file://{profile}]{profile}")
    for source, link_name in parser.get_calculated_paths(name, profile):
        source = os.path.basename(source)
        # print("\t+ {} -> {}".format(source, link_name))
        text_filename = Text(source, "green")
        # text_filename.highlight_regex(r"\..*$", "bold red")
        text_filename.stylize(f"link file://{source}")
        # file_size = path.stat().st_size
        # text_filename.append(f" ({decimal(file_size)})", "blue")
        # icon = "🐍 " if source.suffix == ".py" else "📄 "
        icon = "📄 "
        link_name = un_expanduser(link_name)  # TODO think
        text_filename += Text(" --> ", "blink yellow")
        text_filename += Text(link_name, "yellow")

        tree.add(Text(icon) + text_filename)
