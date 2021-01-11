from os import path
from dotpyle.utils.get_default_path import get_default_path


class TestGetDefaultPath:
    expected_path = path.expanduser("~/.config/dotpyle")

    def test_with_env(self, monkeypatch):
        monkeypatch.setenv("XDG_CONFIG_HOME", "~/.config")
        result_path = get_default_path()

        assert result_path == self.expected_path

    def test_without_env(self):
        result_path = get_default_path()
        assert result_path == self.expected_path
