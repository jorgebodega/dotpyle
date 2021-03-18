dotpyle_ok_cases = [
    {
        "dotfiles": {
            "git": {
                "default": {"before": ["sudo pacman -S git"], "paths": [".gitconfig"]},
                "windows": {
                    "before": ["choco install git.install"],
                    "paths": [".gitconfig"],
                    "root": "C:\\Users\\usr",
                },
            },
            "i3": {
                "default": {
                    "before": ["sudo pacman -S i3"],
                    "paths": [
                        "config",
                        "i3status.conf",
                        "rofitheme.rasi",
                        "i3-resurrect/config.json",
                    ],
                    "root": "~/.config/i3",
                }
            },
            "nvim": {
                "default": {
                    "before": ["sudo pacman -S neovim node"],
                    "paths": ["init.vim", "after/ftplugin/ada.vim"],
                    "root": "~/.config/nvim",
                },
                "windows": {
                    "before": ["choco install neovim --pre"],
                    "paths": ["init.vim", "after/ftplugin/ada.vim"],
                    "root": "C:\\AppData\\Local\\nvim",
                },
            },
        },
        "settings": {"profiles": ["default", "windows"]},
        "version": 0,
    },
    {"version": 1, "settings": {}},
]

dotpyle_error_cases = [
    {
        "version": -1,
    },
    {
        "version": 0,
    },
    {
        "version": 0,
    },
]


dotpyle_hook_ok_cases = [
    "ls",
    "pwd",
    "whoami",
]

dotpyle_hook_error_cases = [
    "thisDoesNotExist",
    "idemNotExistSorry",
    "heheSalut",
]

dotpyle_paths_ok_cases = [{"root": "/tmp", "paths": []}]
