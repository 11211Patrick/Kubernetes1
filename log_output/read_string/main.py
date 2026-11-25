import os
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = int(os.environ.get("PORT", "3000"))
FILE_PATH = os.environ.get("FILE_PATH", "/usr/src/app/files/log.txt")


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/status":
            try:
                with open(FILE_PATH, "rb") as f:
                    body = f.read()
            except FileNotFoundError:
                body = b"No data yet\n"
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