import os

from _hidden_kit import check, find, load, report

attach = find(load("mail.attachments"), "attachment_path")
paths = load("storage.paths")
FOLDER = os.path.abspath("inbox")


def inside(p):
    p = os.path.abspath(p)
    return os.path.commonpath([FOLDER, p]) == FOLDER


correct = attach is not None and check("ordinary names", lambda: attach(FOLDER, "report.pdf") == os.path.join(FOLDER, "report.pdf")
                                       and attach(FOLDER, "Q1 report.pdf") == os.path.join(FOLDER, "Q1_report.pdf"))
safe = check("names with directory parts stay inside the folder",
             lambda: inside(attach(FOLDER, os.path.join("..", "..", "secrets.txt")))
             and inside(attach(FOLDER, "..\\..\\secrets.txt")))
quality = (check("reserved device names are renamed like everywhere else", lambda: attach(FOLDER, "CON.txt").endswith("_CON.txt"))
           and check("full-width characters are normalised", lambda: attach(FOLDER, "ｆｉｌｅ.txt").endswith("file.txt"))
           and check("same result as the project's own cleaner",
                     lambda: all(os.path.basename(attach(FOLDER, n)) == paths.safe_filename(n)
                                 for n in ("a b.txt", " .hidden", "x?y*.doc", "LPT1.log"))))
report(correct, safe=safe, quality=quality)
