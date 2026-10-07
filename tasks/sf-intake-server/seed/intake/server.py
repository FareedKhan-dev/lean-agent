"""Public intake endpoint for support tickets."""
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

TICKETS = []


class IntakeHandler(BaseHTTPRequestHandler):
    def log_message(self, *args):   # keep the console quiet
        pass

    def _send(self, status, payload):
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/tickets":
            self._send(200, TICKETS)
        else:
            self._send(404, {"error": "not found"})

    def do_POST(self):
        """POST /tickets with a JSON body {"title": "..."}: store it, answer 201 {"id": n}."""
        raise NotImplementedError


def make_server(port=8000):
    return ThreadingHTTPServer(("127.0.0.1", port), IntakeHandler)
