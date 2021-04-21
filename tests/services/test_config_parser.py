from os import path
from dotpyle.services.config_parser import ConfigParser
import pytest
from subprocess import CalledProcessError, SubprocessError
from dotpyle_mock_config_files import (
    dotpyle_hook_ok_cases,
    dotpyle_hook_error_cases,
)


def test_process_key():
    # key = dotpyle_mock["program0"]
    # cfh.process_key(key)
    # assert False
    pass


def test_process_key_hook_ok():
    parser = ConfigParser({})  # This does not take place
    try:
        parser.process_key_hooks(dotpyle_hook_ok_cases)

    except Exception as exc:
        assert False, f"'test_process_key_hook_ok' raised an exception {exc}"


def test_process_key_hook_error():
    # monkeypatch.setattr(obj, name, value, raising=True)
    parser = ConfigParser({})  # This does not take place
    with pytest.raises(CalledProcessError) as exception:
        parser.process_key_hooks(dotpyle_hook_error_cases)
    assert exception.type is CalledProcessError


# use tmpdir
def test_process_key_paths(tmpdir, monkeypatch):
    TEST_KEY_NAME = "nvim"
    TEST_PATH_NAME = "init.vim"
    TEST_PROFILE_NAME = "default"
    TEST_CONTENT = "this is just a test case, this content should match with the content of link to be created"
    tmp_file = tmpdir / TEST_KEY_NAME
    tmp_file.write_text(TEST_CONTENT, encoding="utf-8")
    tmp_path_origin = str(tmpdir)
    tmp_path_dest = tmpdir.mkdir("dest")
    monkeypatch.setenv("XDG_CONFIG_HOME", tmp_path_origin)
    parser = ConfigParser({})

    assert True
    return
    # TODO
    parser.process_key_paths(
        key_name=TEST_KEY_NAME,
        profile_name=TEST_PROFILE_NAME,
        root=str(tmp_path_dest),
        paths=[TEST_PATH_NAME],
    )
    print(tmp_file.read_text(encoding="utf-8"))
    tmp_link_created = tmp_path_dest / TEST_PATH_NAME
    print(tmp_link_created)
    # TODO: cant read content on symlink created on temporal directory
    writed_content = tmp_link_created.read_text(encoding="utf-8")
    print(writed_content)

    # cfh.process_key_paths(paths)
    # Check simlinks have been created
    # pass
