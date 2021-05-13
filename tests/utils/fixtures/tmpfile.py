import pytest


@pytest.fixture(scope="session")
def tmpfile(tmpdir_factory):
    tmp_file = tmpdir_factory.mktemp("test").join("test.txt")
    tmp_file.write("")
    return tmp_file
