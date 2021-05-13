{
    "settings": {
        "required": True,
        "type": "dict",
        "schema": {
            "profiles": {
                "required": False,
                "type": "list",
                "default": ["default"],
            }
        },
    },
    "version": {
        "required": True,
        "type": "number",
        "min": 0,
    },
    "dotfiles": {
        "required": False,
        "type": "dict",
        # Define program_name keys
        "keysrules": {"type": "string", "regex": "[a-z,0-9]+"},
        # Values for program_name are dicts with string keys
        "valuesrules": {
            "type": "dict",
            # Define 'profiles' keys
            "keysrules": {"type": "string", "regex": "[a-z,0-9]+"},
            # Define 'profile' values as a dict
            "valuesrules": {
                "type": "dict",
                "schema": {
                    "pre": {"required": False, "type": "list"},
                    "post": {"required": False, "type": "list"},
                    "root": {
                        "required": False,
                        "type": "string",
                        "default": "~",
                    },
                    "paths": {"required": True, "type": "list"},
                },
            },
        },
    },
}
