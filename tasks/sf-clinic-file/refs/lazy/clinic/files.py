import os


def letter_path(patient_folder, filename):
    """The full path of a letter inside the patient's folder."""
    return os.path.join(patient_folder, filename)
