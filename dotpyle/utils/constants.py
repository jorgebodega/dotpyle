import os

APP_NAME = "dotpyle"
DOTPYLE_CONFIG_FILE_NAME = "dotpyle.yml"
DOTPYLE_LOCAL_CONFIG_FILE_NAME = "dotpyle.local.yml"
DOTFILES_FOLDER = "dotfiles"
SCRIPTS_FOLDER = "scripts"
DOTPYLE_CONFIG_FILE_NAME_TEMP = "dotpyle.temp.yml"
DOTPYLE_LOCAL_CONFIG_FILE_NAME_TEMP = "dotpyle.local.temp.yml"
README_NAME = "README.md"
README_TEMPLATE_PATH = "dotpyle/templates/readme.md"
CONFIG_TEMPLATE_PATH = "dotpyle/templates/basic-config.yaml"
CONFIG_LOCAL_TEMPLATE_PATH = "dotpyle/templates/local-config.yaml"
GIT_FOLDER = ".git"

CONFIG_SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "schema.json")
CONFIG_MANAGER_ERROR_CODE = 42
FILE_HANDLER_ERROR_CODE = 10
SCRIPTS_EXTENSION = "yaml"
CONFIG_CHECKER_PROVIDER = "CONFIG_CHECKER"
CONFIG_MANAGER_PROVIDER = "CONFIG_MANAGER_PROVIDER"
REPO_HANDLER_PROVIDER = "REPO_HANDLER"
FILE_HANDLER_PROVIDER = "FILE_HANDLER"
CONFIG_HANDLER_PROVIDER = "CONFIG_HANDLER"
LOCAL_FILE_HANDLER_PROVIDER = "LOCAL_FILE_HANDLER_PROVIDER"
LOGGER_PROVIDER = "LOGGER_PROVIDER"
