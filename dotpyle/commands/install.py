import click
from dotpyle.services.file_handler import FileHandler
from dotpyle.services.config_handler import ConfigHandler
from dotpyle.utils.path import get_source_and_link_path


@click.group()
def install():
    """
    Install a dotfile, hook, etc (TBD)
    """
    pass


@install.command()
@click.argument("name")
@click.option("--profile", "-p", default="default", help="profile name")
@click.option("--no-pre", is_flag=True, help="Dont execute pre hooks")
@click.option("--no-post", is_flag=True, help="Dont execute post hooks")
@click.option("--no-hooks", is_flag=True, help="Dont execute pre and post hooks")
def dotfile(name, profile, no_pre, no_post, no_hooks):

    handler = FileHandler()
    parser = ConfigHandler(config=handler.get_config())

    process_pre = not (no_pre or no_hooks)
    process_post = not (no_post or no_hooks)
    parser.process_key(
        key_name=name,
        profile_name=profile,
        process_pre=process_pre,
        process_post=process_post,
    )
