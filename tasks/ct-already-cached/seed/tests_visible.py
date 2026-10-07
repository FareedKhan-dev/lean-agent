from fx.convert import convert

assert convert(1000, "GBP", "EUR") == 1170
assert convert(500, "EUR", "EUR") == 500
print("ok")
