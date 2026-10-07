def unique_tags(tags):
    """The tags with repeats removed, ignoring case: the first spelling of each, in order."""
    first = {}
    for tag in tags:
        first.setdefault(tag.lower(), tag)
    return list(first.values())
