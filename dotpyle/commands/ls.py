import click
import os
import rich
from rich.text import Text
from rich.tree import Tree
from dotpyle.utils.autocompletion import DotfileNamesVarType, ProfileVarType
from dotpyle.decorators.pass_config_handler import pass_config_handler
from dotpyle.decorators.pass_local_handler import pass_local_handler
from dotpyle.decorators.pass_logger import pass_logger
from dotpyle.utils.path import un_expanduser
from dotpyle.services.logger import Logger
from dotpyle.services.config_handler import ConfigHandler
from dotpyle.services.file_handler import LocalFileHandler


@click.command()
@click.argument("name", required=False, type=DotfileNamesVarType())
@click.option("--profile", "-p", help="profile name", type=ProfileVarType())
@click.option(
    "--all", "-a", is_flag=True, help="list all dotfiles (linked or not)"
)
@pass_local_handler
@pass_config_handler
@pass_logger
def ls(
    logger: Logger,
    config_handler: ConfigHandler,
    local_handler: LocalFileHandler,
    name: str,
    profile: str,
    all: bool,
):
    """
    List dotfiles managed by Dotpyle
    """

    dotfiles = config_handler.get_dotfiles()

    tree = Tree(
        "🌲 [b green]dotfiles",
        highlight=True,
        # f"[bold magenta]:open_file_folder:dotfiles",
        guide_style="bold bright_blue",
    )
    # List all
    if all:
        # Filtering by name
        if name:
            if name in dotfiles:
                profiles = dotfiles[name]
                if profile:
                    if profile in profiles:
                        print_dotfiles(
                            tree,
                            name,
                            profile,
                            profiles[profile],
                            config_handler,
                        )
                    else:
                        logger.failure(
                            "Profile {} in {} does not exist".format(
                                profile, name
                            )
                        )

                # Get all profiles for given name
                else:
                    for profile_name, content in profiles.items():
                        print_dotfiles(
                            tree, name, profile_name, content, config_handler
                        )

        # Get all names
        else:
            # Filtering only by profiles
            if profile:
                if not profile in config_handler.get_profiles():
                    logger.failure(
                        'Profile "{}" does not exist'.format(profile)
                    )

                for program_name, profiles in dotfiles.items():
                    if profile in profiles:
                        print_dotfiles(
                            tree,
                            program_name,
                            profile,
                            profiles[profile],
                            config_handler,
                        )

            else:
                for program_name, profiles in dotfiles.items():
                    for profile_name, content in profiles.items():
                        print_dotfiles(
                            tree,
                            program_name,
                            profile_name,
                            content,
                            config_handler,
                        )

    else:
        # TODO filter
        installed_profiles = local_handler.get_installed()
        logger.log(str(installed_profiles))
        for name, profile_name in installed_profiles.items():
            print_dotfiles(tree, name, profile_name, None, config_handler)

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
