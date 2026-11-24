import os
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = int(os.environ.get("PORT", "3000"))
counter = 0


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        global counter
        if self.path == "/pingpong":
            body = f"pong {counter}\n".encode("utf-8")
            counter += 1
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