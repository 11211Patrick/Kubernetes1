import json
import os
import sys
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler


def require_env(name):
    value = os.environ.get(name)
    if not value:
        sys.exit(f"Missing required environment variable: {name}")
    return value


PORT = int(require_env("PORT"))
MAX_LENGTH = int(require_env("TODO_MAX_LENGTH"))
REDIRECT_URL = require_env("REDIRECT_URL")

todos = []


class Handler(BaseHTTPRequestHandler):
    def send(self, status, content_type, body, headers=None):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        for key, value in (headers or {}).items():
            self.send_header(key, value)
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/todos":
            body = json.dumps(todos).encode("utf-8")
            self.send(200, "application/json", body)
        else:
            self.send(404, "text/plain; charset=utf-8", b"Not found\n")

    def do_POST(self):
        if self.path != "/todos":
            self.send(404, "text/plain; charset=utf-8", b"Not found\n")
            return

        length = int(self.headers.get("Content-Length", 0))
        data = self.rfile.read(length).decode("utf-8")
        form = urllib.parse.parse_qs(data)
        todo = form.get("todo", [""])[0].strip()

        if not todo or len(todo) > MAX_LENGTH:
            self.send(400, "text/plain; charset=utf-8",
                      f"Todo must be 1-{MAX_LENGTH} characters\n".encode("utf-8"))
            return

        todos.append(todo)
        print(f"Created todo: {todo}", flush=True)
        self.send(303, "text/plain; charset=utf-8", b"Created\n", {"Location": REDIRECT_URL})


server = HTTPServer(("0.0.0.0", PORT), Handler)
print(f"Server started in port {PORT}", flush=True)
server.serve_forever()