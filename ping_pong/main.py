import os
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = int(os.environ.get("PORT", "3000"))
COUNT_FILE = os.environ.get("COUNT_FILE", "/usr/src/app/files/pingpong.txt")


def load_count():
    try:
        with open(COUNT_FILE) as f:
            return int(f.read().strip() or 0)
    except FileNotFoundError:
        return 0


def save_count(value):
    os.makedirs(os.path.dirname(COUNT_FILE), exist_ok=True)
    tmp = COUNT_FILE + ".tmp"
    with open(tmp, "w") as f:
        f.write(str(value))
    os.replace(tmp, COUNT_FILE)


counter = load_count()


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        global counter
        if self.path == "/pingpong":
            body = f"pong {counter}\n".encode("utf-8")
            counter += 1
            save_count(counter)
            self.send_response(200)
        else:
            body = b"Not found\n"
            self.send_response(404)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


server = HTTPServer(("0.0.0.0", PORT), Handler)
print(f"Server started in port {PORT}, count starts at {counter}", flush=True)
server.serve_forever()