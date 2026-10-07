import string
from dataclasses import dataclass
from enum import Enum


class Strictness(Enum):
    STRICT = "strict"
    LENIENT = "lenient"


@dataclass(frozen=True)
class ValidationResult:
    valid: bool
    reason: str = ""

    def __bool__(self):
        return self.valid


class OctetRule:
    def check(self, octet):
        if not octet or len(octet) > 3:
            return "an octet has 1 to 3 digits"
        if any(ch not in string.digits for ch in octet):
            return "an octet is decimal digits only"
        if len(octet) > 1 and octet[0] == "0":
            return "leading zeros are ambiguous"
        if int(octet) > 255:
            return "an octet is at most 255"
        return ""


class IPv4Validator:
    def __init__(self, strictness=Strictness.STRICT, octet_rule=None):
        self.strictness = strictness
        self.octet_rule = octet_rule or OctetRule()

    def validate(self, text):
        if not isinstance(text, str):
            return ValidationResult(False, "not a string")
        if self.strictness is Strictness.LENIENT:
            text = text.strip()
        parts = text.split(".")
        if len(parts) != 4:
            return ValidationResult(False, "expected four octets")
        for part in parts:
            problem = self.octet_rule.check(part)
            if problem:
                return ValidationResult(False, problem)
        return ValidationResult(True)


def is_ipv4(text):
    """True if `text` is an IPv4 address in dotted form, like 192.168.0.1."""
    return bool(IPv4Validator().validate(text))
