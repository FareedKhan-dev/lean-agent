from _hidden_kit import check, find, load, report

register = load("register")
geo = load("geo")
lookup = find(geo, "lookup_district")


def known_values():
    return (lookup("SW1A 1AA") == "Westminster" and lookup("EH1 1YZ") == "Edinburgh"
            and lookup("ZZ9 9ZZ") is None and lookup("CF10 1BH") == "Cardiff")


def repeats_are_cached():
    register.SCANS = 0
    for _ in range(5):
        lookup("BT1 1AA")
    first = register.SCANS
    for _ in range(5):
        lookup("M1 1AE")
    return first == 1 and register.SCANS == 2


correct = (lookup is not None
           and check("returns the same districts as before", known_values)
           and check("repeated lookups hit the register once per postcode", repeats_are_cached)
           and check("a cached answer is never reused for another postcode",
                     lambda: lookup("EH1 1YZ") == "Edinburgh" and lookup("SW1A 1AA") == "Westminster"))
check("unknown postcodes still return None", lambda: lookup("ZZ1 1ZZ") is None and lookup("ZZ1 1ZZ") is None)
report(correct)
