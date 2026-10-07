from gallery.render import render_card

html = render_card({"url": "/p/1.jpg", "caption": "Sunset", "author": "Ann"})
assert "<figure>" in html and "/p/1.jpg" in html and "Sunset - Ann" in html, html
print("ok")
