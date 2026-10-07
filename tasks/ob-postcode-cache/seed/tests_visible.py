from geo import lookup_district

assert lookup_district("SW1A 1AA") == "Westminster"
assert lookup_district("m1 1ae") == "Manchester"
assert lookup_district("ZZ9 9ZZ") is None
print("ok")
