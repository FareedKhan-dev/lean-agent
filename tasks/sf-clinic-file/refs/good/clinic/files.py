import os


def letter_path(patient_folder, filename):
    """The full path of a letter inside the patient's folder."""
    folder = os.path.abspath(patient_folder)
    path = os.path.abspath(os.path.join(folder, filename))
    if os.path.commonpath([folder, path]) != folder or path == folder:
        raise ValueError(f"not a file inside the patient's folder: {filename!r}")
    return path
