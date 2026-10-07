import os

from clinic.files import letter_path

p = letter_path("records/000042", "referral.pdf")
assert os.path.basename(p) == "referral.pdf", p
print("ok")
