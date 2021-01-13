from os import path
from dotpyle.utils import get_default_path

EXPECTED_PATH = path.expanduser("~/.config/dotpyle")


def test_with_env(monkeypatch):
    monkeypatch.setenv("XDG_CONFIG_HOME", "~/.config")
    result_path = get_default_path()

    assert result_path == EXPECTED_PATH


def test_without_env():
    result_path = get_default_path()
    assert result_path == EXPECTED_PATH
