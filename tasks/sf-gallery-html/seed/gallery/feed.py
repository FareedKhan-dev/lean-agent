from gallery.render import render_card


def render_feed(photos):
    return "\n".join(render_card(p) for p in photos)
