from catalogue.db import connect
from catalogue.search import search_products

assert search_products(connect(), "rug") == ["Rug"]
print("ok")
