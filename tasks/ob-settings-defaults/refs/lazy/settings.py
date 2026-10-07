"""Application settings: built-in defaults, overridable from a JSON file."""
import json

DEFAULTS = {
    "theme": "light",
    "page_size": 20,
    "currency": "GBP",
    "beta_features": False,
}


def load_settings(path):
    """Return the settings: DEFAULTS, overridden by anything the JSON file at `path` sets."""
    try:
        with open(path, encoding="utf-8") as f:
            return {**DEFAULTS, **json.load(f)}
    except FileNotFoundError:
        return dict(DEFAULTS)
