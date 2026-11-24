import os
import threading
import time
import uuid
from datetime import datetime, timezone
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = int(os.environ.get("PORT", "3000"))
RANDOM_STRING = str(uuid.uuid4())   # 啟動時產生一次，存在記憶體


def status_line():
    ts = datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")
    return f"{ts}: {RANDOM_STRING}"


def log_loop():
    while True:
        print(status_line(), flush=True)
        time.sleep(5)


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/status":
            body = (status_line() + "\n").encode("utf-8")
            self.send_response(200)
        else:
            body = b"Not found\n"
            self.send_response(404)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


threading.Thread(target=log_loop, daemon=True).start()   # 背景印 log

server = HTTPServer(("0.0.0.0", PORT), Handler)
print(f"Server started in port {PORT}", flush=True)
server.serve_forever()