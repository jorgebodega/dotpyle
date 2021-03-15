from os import path
from dotpyle.services.ConfigFileHandler import ConfigFileHandler
import pytest
from subprocess import CalledProcessError, SubprocessError
from dotpyle_mock_config_files import dotpyle_ok_cases, dotpyle_error_cases


dotpyle_mock = {
    "program0": {
        "pre": ["echo hey!"],
        "paths": [""],
        "post": [],
    },
    "program1": {
        "pre": ["thisProgramDoesNotExist -ll --version"],
        "paths": [],
        "post": [],
    },
}

cfh = ConfigFileHandler()


def test_check_config():
    cfh = ConfigFileHandler()
    for config_ok_file in dotpyle_ok_cases:
        errors = cfh.check_config(config_file=config_ok_file)
        assert errors == {}

    for config_error_file in dotpyle_error_cases:
        errors = cfh.check_config(config_file=config_error_file)
        assert errors != {}  # TODO improve tests


def test_iterate():
    # cfh.process_config()
    pass
    # assert False


def test_process_key():
    key = dotpyle_mock["program0"]
    cfh.process_key(key)
    # assert False


def test_process_key_hook_ok():
    try:
        hooks = dotpyle_mock["program0"]["pre"]
        cfh.process_key_hooks(hooks)
    except Exception as exc:
        assert False, f"'test_process_key_hook_ok' raised an exception {exc}"


def test_process_key_hook_error():
    # monkeypatch.setattr(obj, name, value, raising=True)
    with pytest.raises(CalledProcessError) as exception:
        hooks = dotpyle_mock["program1"]["pre"]
        cfh.process_key_hooks(hooks)
    assert exception.type is CalledProcessError
    # assert False


# use tmpdir
def test_process_key_paths(tmpdir):
    paths = dotpyle_mock["program0"]["paths"]
    local_path = tmpdir.mkdir("sub").join("test.txt")
    print(local_path)
    # assert False
    # cfh.process_key_paths(paths)
    # Check simlinks have been created
    # pass
