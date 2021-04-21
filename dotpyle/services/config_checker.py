from typing import NewType
from cerberus import Validator


class ConfigChecker:
    """"""

    def __init__(self):
        # Check if we can move schema info to yaml or json
        self.schema = eval(open("dotpyle/services/schema.py", "r").read())

    def check_config(self, config):
        validator = Validator(self.schema)

        validator.validate(config)
        return validator.errors


ConfigCheckerType = NewType("ConfigCheckerType", ConfigChecker)
