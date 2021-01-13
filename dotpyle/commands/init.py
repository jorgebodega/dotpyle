import click
import subprocess
from git import Repo
from os import mkdir, path
from dotpyle.utils import get_default_path, get_default_url

DOTPYLE_FILE = "dotpyle.yml"


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
def init(url, protocol, token):
    """
    This command will clone an existing Git repository on ${XDG_CONFIG_HOME}/dotpyle
    and will check if this repo contains a dotpyle.yml config file, if not,
    a template config file will be createn
    """

    default_path = get_default_path()
    default_url = get_default_url(url, protocol, token)

    Repo.clone_from(default_url, default_path)
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
    dotpyle_path = default_path + DOTPYLE_FILE
    if not path.isfile(dotpyle_path):
        # Create dotpyle config file
        dotpyle_handler = open(dotpyle_path, "w+")
        # TODO copy default file to config file
        dotpyle_handler.write("example")
        dotpyle_handler.close()

        # TODO: Start configuration process...
