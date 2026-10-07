from _hidden_kit import check, find, load, report

unique = find(load("tags"), "unique_tags")
posts = load("posts")

correct = unique is not None and all([
    check("repeats in other cases are dropped",
          lambda: unique(["Python", "python", "PYTHON", "Rust", "rust"]) == ["Python", "Rust"]),
    check("the first spelling and the order are kept", lambda: unique(["b", "a", "B", "c", "A"]) == ["b", "a", "c"]),
    check("no tags, no tags", lambda: unique([]) == []),
    check("posts get clean tag lists", lambda: posts.save_post("Notes", "SQL, sql, Go, go ")["tags"] == ["SQL", "Go"])])
quality = check("German spellings match the way people mean them",
                lambda: unique(["Straße", "STRASSE", "strasse", "Fuß", "FUSS"]) == ["Straße", "Fuß"])
report(correct, quality=quality)
