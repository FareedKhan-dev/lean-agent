from tags import unique_tags


def save_post(title, raw_tags):
    """The post as stored: tags typed as 'a, b, c' become a clean list."""
    return {"title": title, "tags": unique_tags([t.strip() for t in raw_tags.split(",") if t.strip()])}
