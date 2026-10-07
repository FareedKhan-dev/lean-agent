import os

from storage.paths import safe_filename


def attachment_path(folder, filename):
    """Where an incoming attachment is saved: a file inside `folder`."""
    return os.path.join(folder, safe_filename(filename))
