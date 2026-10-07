from html import escape


def render_card(photo):
    """HTML for one photo card: <figure> with the image and '<caption> - <author>'."""
    url, caption, author = (escape(str(photo[k])) for k in ("url", "caption", "author"))
    return (f'<figure><img src="{url}" alt="{caption}">'
            f"<figcaption>{caption} - {author}</figcaption></figure>")
