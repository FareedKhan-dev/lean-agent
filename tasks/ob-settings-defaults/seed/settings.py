"""Application settings: built-in defaults, overridable from a JSON file."""

DEFAULTS = {
    "theme": "light",
    "page_size": 20,
    "currency": "GBP",
    "beta_features": False,
}


def load_settings(path):
    """Return the settings: DEFAULTS, overridden by anything the JSON file at `path` sets."""
    raise NotImplementedError
