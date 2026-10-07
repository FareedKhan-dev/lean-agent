from shop.catalogue import PRODUCTS
from shop.listing import render_listing

page = render_listing(PRODUCTS["lamps"], 3)
assert page.startswith("page 3 of 3: lamp 21"), page
print("ok")
