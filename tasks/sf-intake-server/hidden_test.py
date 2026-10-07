import json
import sys
import threading
import urllib.error
import urllib.request

from _hidden_kit import check, load, report

sys.stderr = open("_server_errors.txt", "w")      # tracebacks from crashing handlers land here
srv_mod = load("intake.server")
server = srv_mod.make_server(0)
threading.Thread(target=server.serve_forever, daemon=True).start()
BASE = f"http://127.0.0.1:{server.server_address[1]}"


def post(body):
    data = body if isinstance(body, bytes) else json.dumps(body).encode()
    req = urllib.request.Request(BASE + "/tickets", data=data, method="POST",
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=5) as r:
            return r.status, json.loads(r.read() or b"null")
    except urllib.error.HTTPError as e:
        return e.code, None
    except Exception as e:
        return type(e).__name__, None


def still_up():
    with urllib.request.urlopen(BASE + "/tickets", timeout=5) as r:
        return r.status == 200


try:
    created = post({"title": "Printer on fire"})
    correct = (check("a ticket is created with 201 and an id", lambda: created[0] == 201 and isinstance(created[1].get("id"), int))
               and check("it appears in the list", lambda: "Printer on fire" in json.dumps(srv_mod.TICKETS))
               and check("a missing title is a 400", lambda: post({})[0] == 400)
               and check("an empty title is a 400", lambda: post({"title": ""})[0] == 400))
    safe = (check("a body of null is a 400, not a crash", lambda: post(b"null")[0] == 400)
            and check("a JSON list is a 400", lambda: post(b"[1, 2]")[0] == 400)
            and check("a body that is not JSON is a 400", lambda: post(b"{oops")[0] == 400)
            and check("a non-text title is a 400", lambda: post({"title": 5})[0] == 400)
            and check("the server still answers afterwards", still_up))
finally:
    server.shutdown()
report(correct, safe=safe)
