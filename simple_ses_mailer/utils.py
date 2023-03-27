import os


def lookup_env(names):
    """
    Look up for names in environment. Returns the first element found.
    """
    for name in names:
        value = os.environ.get(name)
        if value:
            return value
