def build_headers(to, subject):
    """'To: <to>\\r\\nSubject: <subject>\\r\\n'"""
    return f"To: {to}\r\nSubject: {subject}\r\n"
