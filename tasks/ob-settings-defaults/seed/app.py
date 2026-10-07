from settings import load_settings


def describe(path):
    s = load_settings(path)
    return f"{s['theme']} theme, {s['page_size']} per page, prices in {s['currency']}"
