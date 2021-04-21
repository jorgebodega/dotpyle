import pytest
from dotpyle.services.config_checker import ConfigChecker


@pytest.fixture(scope="session")
def config_checker():
    return ConfigChecker()