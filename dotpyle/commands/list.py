import click
from dotpyle.services.config_handler import ConfigHandler
from dotpyle.services.config_parser import ConfigParser
from dotpyle.utils.path import get_source_and_link_path
import os
import pathlib
import sys

import rich
from rich.filesize import decimal
from rich.markup import escape
from rich.text import Text
from rich.tree import Tree


config = ConfigHandler().get_config()
parser = ConfigParser(config)


@click.command()
@click.option("--name", "-n", help="program name")
@click.option("--profile", "-p", help="profile name")
def list(name, profile):

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
                    print_dotfiles(tree, name, profile, profiles[profile])
                else:
                    print("Profile {} in {} does not exist".format(profile, name))

            # Get all profiles for given name
            else:
                for profile_name, content in profiles.items():
                    print_dotfiles(tree, name, profile_name, content)

    # Get all names
    else:
        # Filtering only by profiles
        if profile:
            for program_name, profiles in dotfiles.items():
                if profile in profiles:
                    print_dotfiles(tree, program_name, profile, profiles[profile])

        else:
            for program_name, profiles in dotfiles.items():
                for profile_name, content in profiles.items():
                    print_dotfiles(tree, program_name, profile_name, content)

    rich.print(tree)


def print_dotfiles(tree, name, profile, content):
    tree = tree.add(f"[bold magenta]:open_file_folder:[link file://{name}]{name}")
    tree = tree.add(f"[bold blue]:open_file_folder:[link file://{profile}]{profile}")
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

        text_filename += Text(" --> ", "blink yellow")
        text_filename += Text(link_name, "yellow")

        tree.add(Text(icon) + text_filename)
