import pytest


@pytest.fixture(scope="session")
def tmpfile(tmpdir_factory):
    tmp_file = tmpdir_factory.mktemp("dotpyle").join("dotpyle.yaml")
    tmp_file.write("")
    return tmp_file
