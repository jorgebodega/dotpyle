import click

from dotpyle.services.file_handler import FileHandler, LocalFileHandler
from dotpyle.decorators.pass_config_handler import pass_config_handler
from dotpyle.decorators.pass_repo_handler import pass_repo_handler

# FIXME: when config file is empty, an error is returned
# TypeError: argument of type 'NoneType' is not iterable
@click.command()
@pass_config_handler
@pass_repo_handler
@click.help_option(help="Add file to dotpyle")
@click.argument("name")
@click.option("--profile", "-p", default="default", help="Profile name, must exist")
@click.option("--root", "-r", default="~", help="Root path")
@click.option(
    "--path",
    multiple=True,
    help="Program dotfiles paths starting from root path",
)
# TODO: make this optional and add everything inside root
@click.option(
    "--pre",
    multiple=True,
    help="Bash command(s) to be executed before installing configuration",
)
@click.option(
    "--post",
    multiple=True,
    help="Bash command(s) to be executed after installing configuration",
)
@click.option(
    "--not-install",
    default=False,
    is_flag=True,
    help="Add files to Dotpyle repo and remove them from original location (useful if user wants to install it afterwards, see dotpyle install)",
)
# @click.option("--pre-hook", multiple=True,  help="Program dotfiles paths starting from root path")
def dotfile(config_handler, repo_handler, name, profile, root, path, pre, post, not_install):
    """ Add DOTFILE to KEY group on Dotpyle tracker TBD """
    print(name, profile, root, path, pre, post)
    # Convert tuples to lists
    paths = list(path)
    pre_commands = list(pre)
    post_commands = list(post)
    added_paths = config_handler.add_dotfile(
        name,
        profile,
        root,
        paths,
        pre_hooks=pre_commands,
        post_hooks=post_commands,
    )
    file_handler = FileHandler()
    # Save modified dotpyle config file
    file_handler.save(config_handler.config)
    # When new key is added to dotpyle, a commit should be generated
    # (adding new files), to keep consistency between yaml and repo

    repo_handler.add(added_paths, config_file_changed=True)
    commit_message = "[dotpyle]: added {} on {} profile on {} program".format(
        added_paths, profile, name
    )
    repo_handler.commit(commit_message)

    if not not_install:
        local_handler = LocalFileHandler()
        local_handler.install_profile(name, profile)
        local_handler.save()

        config_handler.install_key(
            key_name=name, profile_name=profile, process_pre=False, process_post=False
        )
