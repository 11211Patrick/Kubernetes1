import os
import urllib.request
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = int(os.environ.get("PORT", "3000"))
FILE_PATH = os.environ.get("FILE_PATH", "/usr/src/app/files/log.txt")
PINGPONG_URL = os.environ.get("PINGPONG_URL", "http://ping-pong-svc:2346/pings")


def last_line():
    try:
        with open(FILE_PATH) as f:
            lines = f.read().strip().splitlines()
            return lines[-1] if lines else "No data yet"
    except FileNotFoundError:
        return "No data yet"


def ping_count():
    try:
        with urllib.request.urlopen(PINGPONG_URL, timeout=3) as resp:
            return resp.read().decode("utf-8").strip()
    except Exception as e:
        print(f"Failed to get ping count: {e}", flush=True)
        return "unavailable"


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/status":
            body = f"{last_line()}.\nPing / Pongs: {ping_count()}\n".encode("utf-8")
            self.send_response(200)
        else:
            body = b"Not found\n"
            self.send_response(404)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


server = HTTPServer(("0.0.0.0", PORT), Handler)
print(f"Server started in port {PORT}", flush=True)
server.serve_forever()