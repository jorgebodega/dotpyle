import click
import subprocess
from git import Repo
from os import mkdir, path, sys
from shutil import rmtree
from dotpyle.utils.path import get_default_path, get_configuration_path
from dotpyle.utils.url import get_default_url

DOTPYLE_FILE = "dotpyle.yml"


def progress_calculator(op_code, cur_count, max_count=None, message=""):
    click.echo("{0}".format(op_code))
    click.echo("{0}".format(cur_count))
    click.echo("{0}".format(max_count))
    click.echo("{0}".format(message))


def force_callback(ctx, param, value):
    if not value:
        ctx.abort()


@click.command()
@click.option(
    "-u", "--url", required=True, help="Git url of existing repo (GitHub, GitLab, ...)"
)
@click.option(
    "-p",
    "--protocol",
    required=True,
    type=click.Choice(["git", "https"]),
    help="Protocol used to clone the repository. Currently only Git and HTTPS are supported (like Github and Gitlab).",
)
@click.option(
    "-t",
    "--token",
    required=False,
    help="Token could be used to clone a repository if it is private and the protocol is HTTPS. If the repository is private but no token provided, it will probably prompt for username/password (depends on service).",
)
@click.option(
    "-b",
    "--branch",
    required=False,
    help="Desired branch of the repository. If not provided, the `default` branch will be used.",
)
@click.option(
    "-f",
    "--force",
    is_flag=True,
    help="Force init of the package. This results that everything that cause an error will be forced to work even if that means that something will be erased.",
)
def init(url, protocol, token, branch, force):
    """
    This command will clone an existing Git repository on ${XDG_CONFIG_HOME}/dotpyle
    and will check if this repo contains a dotpyle.yml config file, if not,
    a template config file will be created.
    """

    default_path = get_default_path()
    default_url = get_default_url(url, protocol, token)

    if path.exists(default_path):
        if force:
            click.secho(
                "Forcing operation. Make sure you know what you are doing!", fg="red"
            )
            click.secho("Removing config folder...", fg="red")
            rmtree(default_path)
        else:
            click.secho("Folder already exists.", fg="red")
            click.secho(
                "If this is an error, please check folder at {0} or try apply instead of init.".format(
                    default_path
                ),
                fg="red",
            )
            sys.exit(1)

    repository = Repo.clone_from(default_url, default_path, progress=None)
    return

    # Check if dotpyle config file exist
    if not path.isdir(default_path):
        # Create config file
        print("Creating ", default_path)
        mkdir(default_path)

    # If token is defined it is mean that repo is private
    if token:
        # git clone https://<token>@github.com/owner/repo.git
        url = url[0:8] + token + "@" + url[9:]
        # Token is not need to be stored, origin url does store it for us

    print("Cloning into ", url)
    # Bring the remote repo
    process = subprocess.Popen(
        ["git", "clone", url, default_path],
        stdout=subprocess.PIPE,
        universal_newlines=True,
    )
    while True:
        output = process.stdout.readline()
        print(output.strip())
        # Do something else
        return_code = process.poll()
        if return_code is not None:
            print("RETURN CODE", return_code)
            # Process has finished, read rest of the output
            for output in process.stdout.readlines():
                print(output.strip())
            break

    # Check if dotpyle exist
    dotpyle_path = get_configuration_path()
    if not path.isfile(dotpyle_path):
        # Create dotpyle config file
        dotpyle_handler = open(dotpyle_path, "w+")
        # TODO copy default file to config file
        dotpyle_handler.write("example")
        dotpyle_handler.close()

        # TODO: Start configuration process...
