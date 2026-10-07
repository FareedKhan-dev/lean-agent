import json
import threading
import urllib.request

from intake import server

srv = server.make_server(0)
threading.Thread(target=srv.serve_forever, daemon=True).start()
url = f"http://127.0.0.1:{srv.server_address[1]}/tickets"
req = urllib.request.Request(url, data=json.dumps({"title": "Printer on fire"}).encode(), method="POST")
with urllib.request.urlopen(req) as r:
    assert r.status == 201 and "id" in json.loads(r.read())
srv.shutdown()
print("ok")
