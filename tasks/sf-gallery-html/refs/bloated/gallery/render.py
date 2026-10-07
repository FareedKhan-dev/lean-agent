from html import escape


class Node:
    def render(self):
        raise NotImplementedError


class Text(Node):
    def __init__(self, text):
        self.text = text

    def render(self):
        return escape(str(self.text))


class Element(Node):
    void = {"img", "br", "hr"}

    def __init__(self, tag, attrs=None, children=()):
        self.tag, self.attrs, self.children = tag, attrs or {}, list(children)

    def render(self):
        attrs = "".join(f' {k}="{escape(str(v))}"' for k, v in self.attrs.items())
        if self.tag in self.void:
            return f"<{self.tag}{attrs}>"
        return f"<{self.tag}{attrs}>{''.join(c.render() for c in self.children)}</{self.tag}>"


class CardTemplate:
    def build(self, photo):
        image = Element("img", {"src": photo["url"], "alt": photo["caption"]})
        caption = Element("figcaption", children=[Text(f"{photo['caption']} - {photo['author']}")])
        return Element("figure", children=[image, caption])


def render_card(photo):
    """HTML for one photo card: <figure> with the image and '<caption> - <author>'."""
    return CardTemplate().build(photo).render()
