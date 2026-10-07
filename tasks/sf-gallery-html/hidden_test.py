from html.parser import HTMLParser

from _hidden_kit import check, find, load, report

render = find(load("gallery.render"), "render_card")


class Seen(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags, self.imgs, self.text = [], [], ""

    def handle_starttag(self, tag, attrs):
        self.tags.append(tag)
        if tag == "img":
            self.imgs.append(dict(attrs))

    def handle_data(self, data):
        self.text += data


def parse(photo):
    p = Seen()
    p.feed(render(photo))
    return p


ok = {"url": "/p/1.jpg", "caption": "Sunset", "author": "Ann"}
evil = {"url": '/p/2.jpg" onerror="steal()', "caption": "<script>steal()</script>", "author": '<img src=x onerror="steal()">'}
correct = render is not None and check("the card shows the image and the caption line", lambda: (
    parse(ok).imgs and parse(ok).imgs[0].get("src") == "/p/1.jpg" and "Sunset - Ann" in parse(ok).text))
safe = (check("user text cannot add tags or handlers", lambda: (
            "script" not in parse(evil).tags and len(parse(evil).imgs) == 1
            and "onerror" not in parse(evil).imgs[0]))
        and check("every image has alt text (accessibility)",
                  lambda: all((img.get("alt") or "").strip() for img in parse(ok).imgs)))
report(correct, safe=safe)
