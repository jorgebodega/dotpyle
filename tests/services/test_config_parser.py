from os import path
from dotpyle.services.config_parser import ConfigParser
import pytest
from subprocess import CalledProcessError, SubprocessError
from dotpyle_mock_config_files import dotpyle_ok_cases, dotpyle_error_cases, dotpyle_hook_ok_cases, dotpyle_hook_error_cases


def test_check_config_ok():
    for config_ok_file in dotpyle_ok_cases:
        parser = ConfigParser(config_ok_file)
        errors = parser.check_config()
        assert errors == {}

def test_check_config_error():
    for config_error_file in dotpyle_error_cases:
        parser = ConfigParser(config_error_file)
        errors = parser.check_config()
        assert errors != {}  # TODO improve tests

def test_process_key():
    # key = dotpyle_mock["program0"]
    # cfh.process_key(key)
    # assert False
    pass


def test_process_key_hook_ok():
    parser = ConfigParser({}) # This does not take place
    try:
        parser.process_key_hooks(dotpyle_hook_ok_cases)

    except Exception as exc:
        assert False, f"'test_process_key_hook_ok' raised an exception {exc}"


def test_process_key_hook_error():
    # monkeypatch.setattr(obj, name, value, raising=True)
    parser = ConfigParser({}) # This does not take place
    with pytest.raises(CalledProcessError) as exception:
        parser.process_key_hooks(dotpyle_hook_error_cases)
    assert exception.type is CalledProcessError


# use tmpdir
def test_process_key_paths(tmpdir, monkeypatch):
    tmp_path_origin = str(tmpdir)
    tmp_path_dest = str(tmpdir.mkdir('dest'))
    monkeypatch.setenv("XDG_CONFIG_HOME", tmp_path_origin)
    parser = ConfigParser({})
    parser.process_key_paths(key_name='nvim', profile_name='default', root='nvim', paths=[tmp_path_dest + '/' + 'init.vim'])
    assert False

    # assert False
    # cfh.process_key_paths(paths)
    # Check simlinks have been created
    # pass

