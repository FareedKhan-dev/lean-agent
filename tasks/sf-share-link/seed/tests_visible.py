from sharing.links import make_link, open_link

token = make_link("doc42", 2_000_000_000, "s3cret")
assert open_link(token, "s3cret", 1_900_000_000) == "doc42"
print("ok")
