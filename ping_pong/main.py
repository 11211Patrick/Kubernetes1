import os
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = int(os.environ.get("PORT", "3000"))
counter = 0


class Handler(BaseHTTPRequestHandler):
    def send(self, status, body):
        self.send_response(status)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        global counter
        if self.path == "/pingpong":
            body = f"pong {counter}\n".encode("utf-8")
            counter += 1
            self.send(200, body)
        elif self.path == "/pings":
            self.send(200, f"{counter}\n".encode("utf-8"))
        else:
            self.send(404, b"Not found\n")


server = HTTPServer(("0.0.0.0", PORT), Handler)
print(f"Server started in port {PORT}", flush=True)
server.serve_forever()