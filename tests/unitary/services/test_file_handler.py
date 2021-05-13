from os import path
from os.path import isfile
import pytest
from subprocess import CalledProcessError, SubprocessError
from dotpyle.services.file_handler import FileHandler
from tests.utils.fixtures.tmpfile import tmpfile


@pytest.mark.skip()
def test_file_handler_no_path(tmpdir, monkeypatch):
    handler = FileHandler()

    # errors = checker.check_config(config)
    # assert len(errors) == 0


def test_file_handler_with_file_path(tmpfile):
    print(str(tmpfile), isfile(str(tmpfile)))
    handler = FileHandler(str(tmpfile))

    assert handler is not None
    assert handler.stream is not None
    assert handler.config is None
    # errors = checker.check_config(config)
    # assert len(errors) == 0


@pytest.mark.skip()
def test_file_handler_with_dir_path(tmpdir, printer):
    tmp_dir_path = tmpdir
    printer(tmp_file_path)

    handler = FileHandler(tmp_dir_path)

    # errors = checker.check_config(config)
    # assert len(errors) == 0


# def test_check_config_invalid_configs(config):
#     checker = ConfigChecker()

#     errors = checker.check_config(config)
#     assert len(errors) > 0
