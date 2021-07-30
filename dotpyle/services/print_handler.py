from rich.console import Console
from rich.tree import Tree

console = Console(color_system="auto")


def error(*args):
    console.print("Error:", style="red bold", end=" ")
    console.print(*args, style="bold")


def warning(*args):
    console.print("Warning:", style="yellow bold", end=" ")
    console.print(*args, style="bold")


def ok(*args):
    console.print("Success:", style="green bold", end=" ")
    console.print(*args, style="")


def print(*args):
    console.print(*args, style="bold")
    # console.print('hola', style="blink")

    """
    {
        'dotfiles': [
                        {
                            'test': [
                                {
                                    'default': [
                                        {
                                            'paths': [
                                                'required field'
                                                ],
                                            'pathsss': [
                                                'unknown field'
                                                ]
                                            }
                                        ]
                                    }
                                ]
                            }
                    ],
        'version': [
                'min value is 0'
            ]
     }


    dotfiles
        test
            default
                paths: required field
                pathsss: unknown field
    version
        min value 0
    """


def print_config_errors(errors):
    tree = Tree(
        "🌲 [b red]Errors",
        highlight=True,
        guide_style="bold bright_blue",
    )

    for key, value in errors.items():
        # print('out', key, value)
        tree.add(f"[bold yellow]:open_file_folder:[link file://{key}]{key}")
        get_error(tree, key, value)
    print(tree)


# TODO: move this to ConfigParser and create exceptions
def get_error(tree, key, value):
    print(key, value)
    if type(value) == list:
        for elem in value:
            print("list", elem)
            get_error(tree, key, elem)
    elif type(value) == dict:
        for k, v in value.items():
            tree = tree.add(
                f"[bold blue]:open_file_folder:[link file://{k}]{k}"
            )
            get_error(tree, k, v)
    else:
        # print(" - {}: '{}'".format(key, value))
        tree.add(value)
