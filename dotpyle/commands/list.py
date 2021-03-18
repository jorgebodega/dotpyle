import click
from dotpyle.services.config_handler import ConfigHandler
from dotpyle.services.config_parser import ConfigParser
from dotpyle.utils.get_source_and_link_path import get_source_and_link_path


config = ConfigHandler().get_config()
parser = ConfigParser(config)

@click.command()
@click.option('--name', '-n', help='program name')
@click.option('--profile', '-p', help='profile name')
def list(name, profile):

    dotfiles = parser.get_dotfiles()

    # Filtering by name
    if name:
        if name in dotfiles:
            profiles = dotfiles[name]
            if profile:
                if profile in profiles:
                    print_dotfiles(name, profile, profiles[profile])
                else:
                    print ('Profile {} in {} does not exist'.format(profile, name))

            # Get all profiles for given name
            else:
                for profile_name, content in profiles.items():
                    print_dotfiles(name, profile_name, content)

    # Get all names
    else:
        # Filtering only by profiles
        if profile:
            for program_name, profiles in dotfiles.items():
                if profile in profiles:
                    print_dotfiles(program_name, profile, profiles[profile])

        else:
            for program_name, profiles in dotfiles.items():
                for profile_name, content in profiles.items():
                    print_dotfiles(program_name, profile_name, content)



def print_dotfiles(name, profile, content):
    print('======== {} [{}] ========\n - Installed: {}\n - Dotfiles:'.format(name, profile, True))
    for source, link_name in parser.get_calculated_paths(name, profile):
        print ('\t+ {} -> {}'.format(source, link_name))

    print()
