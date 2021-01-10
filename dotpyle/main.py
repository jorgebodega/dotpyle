import click
import subprocess
from subprocess import Popen, run
from os import getenv, path, mkdir

from commands import help


DOTPYLE_FILE = "dotpyle.yml"


@click.group()
def dotpyle():
    """ Needed to create different commands with different options """
    pass


@click.command()
@click.option(
    "-u", "--url", required=True, help="Git url of existing repo (GitHub, GitLab, ...)"
)
@click.option(
    "-p",
    "--protocol",
    required=True,
    type=click.Choice(["git", "https"]),
    help="Git protocol",
)
@click.option(
    "-t",
    "--token",
    required=False,
    help="Git token required if the Git repo is private",
)
def init(url, protocol, token):
    """
    This command will clone an existing Git repository on ${XDG_CONFIG_HOME}/dotpyle
    and will check if this repo contains a dotpyle.yml config file, if not,
    a template config file will be createn
    """

    default_config_path = get_default_path()
    print("default_config_path: ", default_config_path)

    # Check if dotpyle config file exist
    if not path.isdir(default_config_path):
        # Create config file
        print("Creating ", default_config_path)
        mkdir(default_config_path)

    # If token is defined it is mean that repo is private
    if token:
        # git clone https://<token>@github.com/owner/repo.git
        url = url[0:8] + token + "@" + url[9:]
        # Token is not need to be stored, origin url does store it for us

    print("Cloning into ", url)
    # Bring the remote repo
    process = Popen(
        ["git", "clone", url, default_config_path],
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
    dotpyle_path = default_config_path + DOTPYLE_FILE
    if not path.isfile(dotpyle_path):
        # Create dotpyle config file
        dotpyle_handler = open(dotpyle_path, "w+")
        # TODO copy default file to config file
        dotpyle_handler.write("example")
        dotpyle_handler.close()

        # TODO: Start configuration process...


@click.command()
@click.option("--path", help="Path file")
def add(path):
    pass


@click.command()
def commit():
    pass


@click.command()
def config():
    pass


def get_default_path():
    # Get defautl config path
    # If it does not exist, take .config
    default_config_path = getenv("XDG_CONFIG_HOME", default="~/.config/")
    # Expand ~ home
    default_config_path = path.expanduser(default_config_path)

    default_config_path += "dotpyle/"
    return default_config_path


# Add commands to group
dotpyle.add_command(init)
dotpyle.add_command(add)
dotpyle.add_command(commit)
dotpyle.add_command(config)
dotpyle.add_command(help)


def main():
    dotpyle()


if __name__ == "__main__":
    dotpyle()
