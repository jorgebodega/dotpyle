"""Dotpyle exceptions definition"""

from dotpyle.utils import constants


class DotpyleException(Exception):
    """Dotpyle generic exception"""

    def __init__(self, message: str = "", code: int = 1):
        self.message = message
        self.code = code
        super().__init__(self.message)


class FileHandlerException(DotpyleException):
    """FileHandler custom exception"""

    def __init__(self, message: str):
        super().__init__(message, constants.FILE_HANDLER_ERROR_CODE)


class ConfigManagerException(DotpyleException):
    """ConfigManager custom exception"""

    def __init__(self, message: str):
        message = "[CONFIG] " + message
        super().__init__(message, constants.CONFIG_MANAGER_ERROR_CODE)
