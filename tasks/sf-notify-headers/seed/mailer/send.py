from mailer.headers import build_headers


def message(to, subject, body):
    return build_headers(to, subject) + "\r\n" + body
