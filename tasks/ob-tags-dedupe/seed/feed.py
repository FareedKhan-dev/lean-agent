def tag_cloud(posts):
    """(tag, number of posts) pairs, most used first."""
    counts = {}
    for post in posts:
        for tag in post["tags"]:
            counts[tag] = counts.get(tag, 0) + 1
    return sorted(counts.items(), key=lambda kv: -kv[1])
