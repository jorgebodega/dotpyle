import json
from collections.abc import Iterable
from cerberus import Validator
from cerberus.errors import ValidationError
from dotpyle import constants


class ConfigChecker:
    """
    This class is a service with only one function: validate the schema
    to avoid unexpected errors.
    """

    def __init__(self):
        with open(constants.CONFIG_SCHEMA_PATH, "r") as schema_file:
            schema = json.loads(schema_file.read())
            self.validator = Validator(schema)

    def check_config(self, config: str) -> Iterable[ValidationError]:
        """
        Check if the provided config match the schema inside the validator.

        Args:
            config (str): User configuration file representation

        Returns:
            Iterable[ValidationError]: Every error found while validating the schema
        """

        self.validator.validate(config)
        return self.validator.errors
