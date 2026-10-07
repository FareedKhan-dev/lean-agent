from mailer.headers import build_headers

assert build_headers("ann@example.org", "Your order") == "To: ann@example.org\r\nSubject: Your order\r\n"
print("ok")
