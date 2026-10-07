import csv

from _hidden_kit import check, load, report

handlers = load("shopfront.api.handlers")
load("shopfront.data").load_demo()


def exported():
    handlers.SERVICES.orders.export_csv("orders.csv")
    with open("orders.csv", newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))
    body = rows[1:]
    return len(body) == 8 and ["1", "ann@example.org", "2499"] in body and any(r[1].lower() == "bo@example.org" for r in body)


correct = check("one row per order with id, email and total, after a header", exported)
report(correct)
