import os


def attachment_path(folder, filename):
    """Where an incoming attachment is saved: a file inside `folder`."""
    return os.path.join(folder, os.path.basename(filename.replace("\\", "/")).replace(" ", "_"))
