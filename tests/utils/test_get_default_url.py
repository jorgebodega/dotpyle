from os import path
from dotpyle.utils import get_default_url

HTTPS_URL = "https://github.com/exampleuser/examplerepo.git"
GIT_URL = "git@github.com:exampleuser/examplerepo.git"
TOKEN = "testtoken"


def test_with_https():
    result_url = get_default_url(HTTPS_URL, "https")

    assert result_url == HTTPS_URL


def test_with_https_with_token():
    result_url = get_default_url(HTTPS_URL, "https", TOKEN)

    expected_url = "{0}{1}@{2}".format(HTTPS_URL[:8], TOKEN, HTTPS_URL[9:])

    assert result_url == expected_url


def test_with_git():
    result_url = get_default_url(GIT_URL, "git")

    assert result_url == GIT_URL
