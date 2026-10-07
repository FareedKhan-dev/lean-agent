def build_headers(to, subject):
    """'To: <to>\\r\\nSubject: <subject>\\r\\n'; refuses line breaks, which would start new headers."""
    if any(ch in value for value in (to, subject) for ch in "\r\n"):
        raise ValueError("header values cannot contain line breaks")
    return f"To: {to}\r\nSubject: {subject}\r\n"
