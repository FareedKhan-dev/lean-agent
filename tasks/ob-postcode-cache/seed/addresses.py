from geo import lookup_district, normalise


def label(name, street, postcode):
    district = lookup_district(postcode) or "Unknown district"
    return f"{name}\n{street}\n{district}\n{normalise(postcode)}"
