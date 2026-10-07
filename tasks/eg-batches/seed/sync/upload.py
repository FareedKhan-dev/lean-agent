from sync.chunks import batches
from sync.db import stock_rows

SENT = []   # stands in for the warehouse API in this repository


def send(records):
    SENT.append(list(records))


def upload_all(conn, size=500):
    for batch in batches(stock_rows(conn), size):
        send(batch)
