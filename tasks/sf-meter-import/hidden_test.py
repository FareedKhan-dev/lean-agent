from _hidden_kit import check, find, load, report

total = find(load("meters.importer"), "total_kwh")


def write(name, text):
    with open(name, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    return name


clean = write("clean.csv", "meter_id,kwh\nm1,100.5\nm2,200\nm3,50.5\n")
dirty = write("dirty.csv", "meter_id,kwh\nm1,100.5\nm2,200\nm4,N/A\nm5,\nm6\nm3,50.5\n")
correct = total is not None and check("a clean export", lambda: abs(total(clean) - 351.0) < 1e-6)
safe = check("bad rows are skipped and the good ones still counted", lambda: abs(total(dirty) - 351.0) < 1e-6)
report(correct, safe=safe)
