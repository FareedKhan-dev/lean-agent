"""Application settings: built-in defaults, overridable from a JSON file."""
import json
import os
from dataclasses import asdict, dataclass, field, fields


class SettingsError(ValueError):
    """Raised when a settings file cannot be used."""


@dataclass
class Settings:
    theme: str = "light"
    page_size: int = 20
    currency: str = "GBP"
    beta_features: bool = False
    extra: dict = field(default_factory=dict)

    @classmethod
    def from_mapping(cls, data):
        known = {f.name for f in fields(cls)} - {"extra"}
        settings = cls(**{k: v for k, v in data.items() if k in known})
        settings.extra = {k: v for k, v in data.items() if k not in known}
        return settings

    def apply_env(self, prefix="APP_"):
        for f in fields(self):
            value = os.environ.get(prefix + f.name.upper())
            if value is not None and f.name != "extra":
                setattr(self, f.name, type(getattr(self, f.name))(value))
        return self

    def to_dict(self):
        out = asdict(self)
        out.update(out.pop("extra"))
        return out


DEFAULTS = Settings().to_dict()


class SettingsLoader:
    """Reads and validates a settings file."""

    def __init__(self, path):
        self.path = path

    def read(self):
        if not os.path.exists(self.path):
            return {}
        try:
            with open(self.path, encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            raise SettingsError(f"{self.path}: not valid JSON ({e})") from e
        if not isinstance(data, dict):
            raise SettingsError(f"{self.path}: expected a JSON object")
        return data

    def load(self):
        return Settings.from_mapping(self.read()).apply_env().to_dict()


def load_settings(path):
    """Return the settings: DEFAULTS, overridden by anything the JSON file at `path` sets."""
    return SettingsLoader(path).load()
