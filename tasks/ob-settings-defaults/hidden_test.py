from _hidden_kit import check, load, report

s = load("settings")
DEFAULTS = {"theme": "light", "page_size": 20, "currency": "GBP", "beta_features": False}


def write(name, text):
    with open(name, "w", encoding="utf-8") as f:
        f.write(text)
    return name


def rejected_with_name(text, name):
    path = write(name, text)
    try:
        s.load_settings(path)
    except ValueError as e:
        return name in str(e)
    return False


correct = (check("file values override defaults, the rest stay",
                 lambda: s.load_settings(write("a.json", '{"theme": "dark", "page_size": 50}'))
                 == {**DEFAULTS, "theme": "dark", "page_size": 50})
           and check("a missing file gives the defaults", lambda: s.load_settings("no_such_file.json") == DEFAULTS)
           and check("keys the defaults do not know are kept",
                     lambda: s.load_settings(write("b.json", '{"region": "eu"}'))["region"] == "eu"))
quality = (check("invalid JSON: ValueError naming the file",
                 lambda: rejected_with_name("{theme: dark", "broken_settings.json"))
           and check("JSON null: ValueError naming the file", lambda: rejected_with_name("null", "null_settings.json"))
           and check("a JSON list: ValueError naming the file", lambda: rejected_with_name("[1, 2]", "list_settings.json")))
report(correct, quality=quality)
