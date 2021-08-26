import click
from dotpyle.utils.path import get_source_and_link_path
from dotpyle.services.print_handler import error, warning, ok
from dotpyle.decorators.pass_config_handler import pass_config_handler
from dotpyle.decorators.pass_local_handler import pass_local_handler
from dotpyle.decorators.pass_logger import pass_logger


@click.command()
@click.argument("name")
@click.option("--profile", "-p", default="default", help="profile name")
@click.option("--no-pre", is_flag=True, help="Dont execute pre hooks")
@click.option("--no-post", is_flag=True, help="Dont execute post hooks")
@click.option(
    "--no-hooks", is_flag=True, help="Dont execute pre and post hooks"
)
@pass_local_handler
@pass_config_handler
@pass_logger
def link(
    logger,
    config_handler,
    local_handler,
        name, profile, no_pre, no_post, no_hooks):

    if local_handler.is_profile_installed(name, profile):
        error("Profile {} already installed for {}".format(profile, name))
        return

    process_pre = not (no_pre or no_hooks)
    process_post = not (no_post or no_hooks)
    config_handler.install_key(
        key_name=name,
        profile_name=profile,
        process_pre=process_pre,
        process_post=process_post,
    )
    local_handler.install_profile(name, profile)
    local_handler.save(local_handler.config)
    ok("{} dotfiles installed".format(name))
