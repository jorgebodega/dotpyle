from dotpyle.utils.get_default_path import get_default_path


# Aww yes global variable!
dotpyle_path = get_default_path()


def get_source_and_link_path(name, profile, root, path):
    source = "{0}/dotfiles/{1}/{2}/{3}".format(dotpyle_path, name, profile, path)
    link_name = root + "/" + path

    return source, link_name
