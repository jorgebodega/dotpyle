valid_cases = [
    {
        "dotfiles": {
            "git": {
                "default": {"pre": ["sudo pacman -S git"], "paths": [".gitconfig"]},
                "windows": {
                    "pre": ["choco install git.install"],
                    "paths": [".gitconfig"],
                    "root": "C:\\Users\\usr",
                },
            },
            "i3": {
                "default": {
                    "pre": ["sudo pacman -S i3"],
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
                    "pre": ["sudo pacman -S neovim node"],
                    "paths": ["init.vim", "after/ftplugin/ada.vim"],
                    "root": "~/.config/nvim",
                },
                "windows": {
                    "pre": ["choco install neovim --pre"],
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