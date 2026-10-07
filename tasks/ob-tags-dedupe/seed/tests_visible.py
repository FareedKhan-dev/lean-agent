from tags import unique_tags

assert unique_tags(["Python", "python", "Rust"]) == ["Python", "Rust"]
print("ok")
