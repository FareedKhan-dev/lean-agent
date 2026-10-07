from clinic.files import letter_path


def save_letter(patient_folder, filename, data):
    with open(letter_path(patient_folder, filename), "wb") as f:
        f.write(data)
