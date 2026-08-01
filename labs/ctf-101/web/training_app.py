"""Local-only teaching app for HTTP, session, and authorization lessons."""

from __future__ import annotations

import json
from http import cookies
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse


DOCUMENTS = {
    "doc-a": {"owner": "alice", "content": "Alice 的本地教学记录"},
    "doc-b": {"owner": "bob", "content": "Bob 的本地教学记录"},
}
USERS = {"alice": {"role": "member"}, "bob": {"role": "member"}, "teacher": {"role": "admin"}}


class Handler(BaseHTTPRequestHandler):
    server_version = "CTF101Local/1.0"

    def send_json(self, status: int, payload: dict, headers: dict[str, str] | None = None):
        body = json.dumps(payload, ensure_ascii=False, indent=2).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        for name, value in (headers or {}).items():
            self.send_header(name, value)
        self.end_headers()
        self.wfile.write(body)

    def current_user(self) -> str | None:
        jar = cookies.SimpleCookie(self.headers.get("Cookie", ""))
        morsel = jar.get("training_session")
        return morsel.value if morsel and morsel.value in USERS else None

    def do_GET(self):
        parsed = urlparse(self.path)
        query = parse_qs(parsed.query)

        if parsed.path == "/":
            self.send_json(
                200,
                {
                    "service": "CTF 101 local training app",
                    "routes": ["/login?user=alice", "/profile", "/document?id=doc-a"],
                    "boundary": "127.0.0.1 only",
                },
            )
            return

        if parsed.path == "/login":
            user = query.get("user", [""])[0]
            if user not in USERS:
                self.send_json(400, {"error": "unknown training user"})
                return
            self.send_json(
                200,
                {"logged_in_as": user},
                {"Set-Cookie": f"training_session={user}; HttpOnly; SameSite=Lax"},
            )
            return

        user = self.current_user()
        if user is None:
            self.send_json(401, {"error": "login required"})
            return

        if parsed.path == "/profile":
            self.send_json(200, {"id": user, **USERS[user]})
            return

        if parsed.path == "/document":
            document_id = query.get("id", [""])[0]
            document = DOCUMENTS.get(document_id)
            if document is None:
                self.send_json(404, {"error": "document not found"})
                return
            if USERS[user]["role"] != "admin" and document["owner"] != user:
                self.send_json(403, {"error": "forbidden"})
                return
            self.send_json(200, {"id": document_id, **document})
            return

        self.send_json(404, {"error": "route not found"})


def main() -> None:
    server = ThreadingHTTPServer(("127.0.0.1", 8081), Handler)
    print("CTF 101 local app: http://127.0.0.1:8081")
    server.serve_forever()


if __name__ == "__main__":
    main()
