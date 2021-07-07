import pytest
from yaml import safe_dump
from dotpyle.errors.InvalidConfigFile import InvalidConfigFileError
from dotpyle.services.config_handler import ConfigHandler
from tests.utils.mocks.config_valid_cases import valid_cases


def test_init_no_path(tmpdir, monkeypatch):
    tmpdir.mkdir("dotpyle").join("dotpyle.yml").write("")
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmpdir))

    handler = ConfigHandler()

    assert handler is not None


def test_init_with_file_path(tmpdir):
    tmpfile = tmpdir.mkdir("dotpyle").join("dotpyle.yml")
    tmpfile.write("")
    handler = ConfigHandler(str(tmpfile))

    assert handler is not None


def test_init_with_dir_path(tmpdir):
    with pytest.raises(InvalidConfigFileError):
        assert ConfigHandler(tmpdir)


@pytest.mark.parametrize("config", [*valid_cases])
def test_read(tmpdir, config):
    dumped_data = safe_dump(config)
    tmpfile = tmpdir.mkdir("dotpyle").join("dotpyle.yml")
    tmpfile.write(dumped_data)

    handler = ConfigHandler(str(tmpfile))

    config_read = handler.read()

    assert config_read is not None
    assert config_read == config
