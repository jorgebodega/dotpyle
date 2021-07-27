import pytest
from tests.utils.mocks.config_valid_cases import valid_cases
from tests.utils.mocks.config_invalid_cases import invalid_cases
from dotpyle.services.config_checker import ConfigChecker


@pytest.mark.parametrize("config", [*valid_cases])
def test_config_checker_valid_configs(config):
    """Test that the config checker returns True when given valid configs."""

    checker = ConfigChecker()

    errors = checker.check_config(config)
    assert len(errors) == 0


@pytest.mark.parametrize("config", [*invalid_cases])
def test_config_checker_invalid_configs(
    config,
):
    """Test that the config checker returns errors when given invalid configs."""

    checker = ConfigChecker()

    errors = checker.check_config(config)
    assert len(errors) > 0
