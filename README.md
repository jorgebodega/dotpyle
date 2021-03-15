# dotpyle

Dotpyle is a Python implementation of a dotfile system manager, allowing users
to keep a secure copy of all program configurations remotly, create different
profiles, etc.

## TBD

dotpyle.yml organization:

key:
    before: ...
    after: ...
    paths:
        - symlink0:fileInsideKeyFolder0
        - symlink1:fileInsideKeyFolder1
        - filename

This will traduce into:

- dotfiles
    - key
        - fileInsideKeyFolder0   ==> ln -s symlink0
        - fileInsideKeyFolder1   ==> ln -s symlink0
        - filename

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


### Push

### List of commands
    dotpyle init
    dotpyle add [file | pre-hook | post-hook]
    dotpyle  [file | pre-hook | post-hook]


### Dotpyle.yml example

Structure of yml (every thing inside [] are examples)

```

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

```
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
dotpyle repo file structure
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
