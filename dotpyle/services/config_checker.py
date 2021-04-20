from typing import NewType
import cerberus


class ConfigChecker:
    """"""

    def __init__(self):
        self.schema = eval(open("dotpyle/services/schema.py", "r").read())

    def check_config(self, config):
        validator = cerberus.Validator(self.schema)
        validator.validate(config)

        return validator.errors


ConfigCheckerType = NewType("ConfigCheckerType", ConfigChecker)


class ConfigCheckerDecorator:
    """"""

    def __init__(self, arg):
        self._arg = arg
        self.checker = ConfigChecker()

    def __call__(self, *args, **kwargs):
        instance = self._arg.__new__(self._arg)
        instance.checker = self.checker
        instance.__init__(*args, **kwargs)

        return instance
