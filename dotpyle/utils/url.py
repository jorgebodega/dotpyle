from enum import Enum


class Protocol(Enum):
    HTTPS = "https"
    GIT = "git"


def get_default_url(url: str, protocol: Protocol, token: str = None):
    """
    Format the repository URL.

    Because of the repo could be public or private, and can be used with two different protocols,
    need to calculate a definitive URL to clone the content.
    """
    default_url = url

    if protocol == "https" and token is not None:
        default_url = "{0}{1}@{2}".format(url[:8], token, url[9:])

    return default_url
