def render_card(photo):
    """HTML for one photo card: <figure> with the image and '<caption> - <author>'."""
    return (f'<figure><img src="{photo["url"]}">'
            f'<figcaption>{photo["caption"]} - {photo["author"]}</figcaption></figure>')
