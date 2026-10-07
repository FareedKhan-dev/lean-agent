import os

from _hidden_kit import check, find, load, report

letter_path = find(load("clinic.files"), "letter_path")
FOLDER = os.path.abspath(os.path.join("records", "000042"))
UP = ".."


def inside(name):
    """The name is either refused, or it resolves inside the patient's folder."""
    try:
        p = os.path.abspath(letter_path(FOLDER, name))
    except Exception:
        return True
    return os.path.commonpath([FOLDER, p]) == FOLDER and p != FOLDER


attacks = [os.path.join(UP, UP, "secrets.txt"), "\\".join([UP, UP, "secrets.txt"]),
           "/".join(["a", UP, UP, UP, "secrets.txt"]), os.path.abspath(os.sep + os.path.join("etc", "hosts")),
           "C:" + "\\".join(["", "Windows", "win.ini"])]
correct = letter_path is not None and check("an ordinary letter lands in the folder", lambda: (
    os.path.dirname(os.path.abspath(letter_path(FOLDER, "referral.pdf"))) == FOLDER
    and os.path.basename(letter_path(FOLDER, "referral.pdf")) == "referral.pdf"))
safe = check("no uploaded name can escape the patient's folder", lambda: all(inside(a) for a in attacks))
report(correct, safe=safe)
