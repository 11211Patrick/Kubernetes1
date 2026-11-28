import os
import urllib.request
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = int(os.environ.get("PORT", "3000"))
FILE_PATH = os.environ.get("FILE_PATH", "/usr/src/app/files/log.txt")
INFO_FILE = os.environ.get("INFO_FILE", "/usr/src/app/config/information.txt")
PINGPONG_URL = os.environ.get("PINGPONG_URL", "http://ping-pong-svc:2346/pings")


def last_line():
    try:
        with open(FILE_PATH) as f:
            lines = f.read().strip().splitlines()
            return lines[-1] if lines else "No data yet"
    except FileNotFoundError:
        return "No data yet"


def info_file_content():
    try:
        with open(INFO_FILE) as f:
            return f.read().strip()
    except FileNotFoundError:
        return "(file not found)"


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
            message = os.environ.get("MESSAGE", "")
            body = (
                f"file content: {info_file_content()}\n"
                f"env variable: MESSAGE={message}\n"
                f"{last_line()}.\n"
                f"Ping / Pongs: {ping_count()}\n"
            ).encode("utf-8")
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