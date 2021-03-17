# dotpyle

Dotpyle is a Python implementation of a dotfile system manager, allowing users
to keep a secure copy of all program configurations remotly, create different
profiles, etc.


## Commands

### Init

This will request a git url and a git token If it is the first time you use
Dotpyle, you will need to create an empty repo on GitHub, GitLab, etc.

If you want to manage an existing repo you just need to input url and token

    dotpyle init [--url <git url>]  [--protocol (git/https)] [--token (if repo is private)]


### Add

    dotpyle add [--path PATH] [OPTS]

1. Copy file to repo location
2. Delete file of path
3. Generate symbolic link to path

Examples:

1. Create program_name key
1. Create profile (default by default)
1. Set root and paths (optionally pre and post hooks)

```sh
    dotpyle add <program_name> [--profile=<profile_name>]
    dotpyle set <program_name> [--profile=<profile_name>] [root=<root_path>] [paths=<dotfile_path1:dotfile_path2:...>]

    dotpyle dotfiles add [--profile=<profile_name>] [--root=<root_path>] paths=[<dotfile_path>, ...]
```

### List

    dotpyle list [--name=<program_name>] [--profile=<profile_name>]


### Push

### List of commands

    dotpyle init
    dotpyle add [file | pre-hook | post-hook]
    dotpyle  [file | pre-hook | post-hook]

### Profiles

#### profile create

    dotpyle profile create <profile_name>

Creates a new profile named `<profile_name>`, if it does not exist.

#### profile list

    dotpyle profile list [<profile_name>]

#### profile change

    dotpyle profile change <profile_name> [<program_name> ...]

This option will change the configuration file to the `<profile_name>` passed for:

- all dotfiles if no `<program_name>` is passed
- all `<program_name>`'s passed

Example:

    dotpyle profile change work nvim git

Neovim work profile and Git work profile will be symlinked to its corresponding path.

    dotpyle profile change home

All dotfiles which have a 'home' profile will be symlinked to its corresponding paths.
Dotfiles which does not have a configuration for given profile will not be altered.

TBD

### Configuration

#### check

    dotpyle config check [<dotpyle_config_path>]

This command will analize Dotpyle configuration file, by default
(`XDG_CONFIG_HOME}/dotpyle/dotpyle.yml`) (or `<dotpyle_config_path>`),
returning descriptive errors.

**Info**: any other command will anayle the configuration file before
executing.  This command is useful and recomended whenever any manual change is
made on *dotpyle.yml*.


### dotpyle.yml example

Structure of yml (every thing inside [] are examples)

```yaml
# General settings for dotpyle
settings:

    # Defined profiles
    profiles:
        - default
        - [home]
        - [work]

    # TODO
    TBD

dotfiles:

    # Top level key, the name of the program for which store config files
    [program_name]:

        # Name of the profile (default profile: default)
        [profile_name]:

            # Bash commands to be executed before configuring 'profile_name'
            before:
                - [bash script 1]
                - [bash script 2]

            # Bash commands to be executed after configuring 'profile_name'
            after:
                - [bash script 1]
                - [bash script 2]

            # Base path for start storing 'paths' for 'program_name' (default $HOME)
            root: ~

            # Configuration files for 'program_name'. Subroutes will be created if they dont exist
            paths:
                - [.configuration]                # will symlink dotfiles/program_name/profile_name/.configuration => $HOME/.configuration
                - [subroute/.filerc]              # will symlink dotfiles/program_name/profile_name/subroute/.filerc => $HOME/subroute/.filerc
                - [subroute0/subroute1/filerc]    # will symlink dotfiles/program_name/profile_name/subroute0/subroute1/filerc => $HOME/subroute0/subroute1/filerc


```

Example of dotpyle.yml config file:

```yaml
settings:
    profiles:
        - default
        - windows

dotfiles:
    git:
        default:
            before:
                - sudo pacman -S git
            paths:
                - .gitconfig

        windows:
            before:
                - choco install git.install
            root: C:\Users\usr
            paths:
                - .gitconfig

    nvim:
        default:
            before:
                - sudo pacman -S neovim node
            root: ~/.config/nvim
            paths:
                - init.vim
                - after/ftplugin/ada.vim

        windows:
            before:
                - choco install neovim --pre
            root: C:\AppData\Local\nvim
            paths:
                - init.vim
                - after/ftplugin/ada.vim
```

This will be the generated file structure on the repository:

```

dotfiles
|
|-> git
|   |-> default
|   |   |-> .gitconfig
|   |-> windows
|       |-> .gitconfig
|
|-> nvim
    |-> default
    |   |-> init.vim
    |   |-> after
    |       |-> ftplugin
    |           |-> ada.vim
    |
    |-> windows
        |-> init.vim
        |-> after
            |-> ftplugin
                |-> ada.vim
```
