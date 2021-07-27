import click
from os import system, path
from shutil import copy2
from tempfile import gettempdir
from dotpyle.utils.path import get_configuration_path, get_dotpyle_readme_path
from dotpyle.services.config_handler import ConfigHandler
from dotpyle.services.file_handler import FileHandler
from dotpyle.services.repo_handler import RepoHandler
from dotpyle.utils import constants

@click.command()
def readme():
    readme_path = get_dotpyle_readme_path()

    if not path.exists(readme_path):
        # Geterate a README with default template
        copy2(constants.README_TEMPLATE_PATH, readme_path)

    # Open user default editor
    res = click.edit(filename=readme_path)

    repo = RepoHandler()
    repo.add(constants.README_NAME, config_file_changed=False)
