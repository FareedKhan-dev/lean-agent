"""Public intake endpoint for support tickets."""
import json
from dataclasses import dataclass
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

TICKETS = []


class BadRequest(Exception):
    pass


@dataclass
class TicketInput:
    title: str

    @classmethod
    def from_json(cls, raw):
        try:
            data = json.loads(raw or b"null")
        except ValueError as exc:
            raise BadRequest("the body must be JSON") from exc
        if not isinstance(data, dict):
            raise BadRequest("the body must be a JSON object")
        title = data.get("title")
        if not isinstance(title, str) or not title.strip():
            raise BadRequest("a non-empty title is required")
        return cls(title.strip())


class TicketService:
    def create(self, ticket):
        TICKETS.append({"id": len(TICKETS) + 1, "title": ticket.title})
        return len(TICKETS)


class Router:
    def __init__(self):
        self.routes = {}

    def add(self, method, path, handler):
        self.routes[(method, path)] = handler

    def find(self, method, path):
        return self.routes.get((method, path))


class IntakeHandler(BaseHTTPRequestHandler):
    service = TicketService()
    router = Router()

    def log_message(self, *args):   # keep the console quiet
        pass

    def _send(self, status, payload):
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _dispatch(self, method):
        handler = self.router.find(method, self.path)
        if handler is None:
            return self._send(404, {"error": "not found"})
        try:
            status, payload = handler(self)
        except BadRequest as exc:
            status, payload = 400, {"error": str(exc)}
        self._send(status, payload)

    def do_GET(self):
        self._dispatch("GET")

    def do_POST(self):
        """POST /tickets with a JSON body {"title": "..."}: store it, answer 201 {"id": n}."""
        self._dispatch("POST")


def _list(handler):
    return 200, TICKETS


def _create(handler):
    raw = handler.rfile.read(int(handler.headers.get("Content-Length") or 0))
    return 201, {"id": handler.service.create(TicketInput.from_json(raw))}


IntakeHandler.router.add("GET", "/tickets", _list)
IntakeHandler.router.add("POST", "/tickets", _create)


def make_server(port=8000):
    return ThreadingHTTPServer(("127.0.0.1", port), IntakeHandler)
