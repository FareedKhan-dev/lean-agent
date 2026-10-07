import os
from dataclasses import dataclass, field


class PathPolicyError(ValueError):
    """Raised when a path breaks the storage policy."""


@dataclass
class PathPolicy:
    allow_symlinks: bool = False
    max_depth: int = 1
    allowed_extensions: set = field(default_factory=lambda: {".pdf", ".docx", ".txt"})

    def check_extension(self, filename):
        ext = os.path.splitext(filename)[1].lower()
        if self.allowed_extensions and ext not in self.allowed_extensions:
            raise PathPolicyError(f"extension {ext!r} not allowed")


class SafePathResolver:
    """Resolves untrusted filenames inside a base folder according to a policy."""

    def __init__(self, base, policy=None):
        self.base = os.path.abspath(base)
        self.policy = policy or PathPolicy()

    def resolve(self, filename):
        self.policy.check_extension(filename)
        candidate = os.path.abspath(os.path.join(self.base, filename))
        if os.path.commonpath([self.base, candidate]) != self.base or candidate == self.base:
            raise PathPolicyError(f"path escapes the base folder: {filename!r}")
        if not self.policy.allow_symlinks and os.path.islink(candidate):
            raise PathPolicyError("symlinks are not allowed")
        return candidate


def letter_path(patient_folder, filename):
    """The full path of a letter inside the patient's folder."""
    return SafePathResolver(patient_folder).resolve(filename)
