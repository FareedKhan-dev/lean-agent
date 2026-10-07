import os

from mail.attachments import attachment_path

assert attachment_path("inbox", "report.pdf") == os.path.join("inbox", "report.pdf")
print("ok")
