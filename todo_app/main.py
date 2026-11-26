import os
import threading
import time
import urllib.request
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = int(os.environ.get("PORT", "3000"))
IMAGE_DIR = os.environ.get("IMAGE_DIR", "/usr/src/app/files")
IMAGE_PATH = os.path.join(IMAGE_DIR, "image.jpg")
IMAGE_URL = os.environ.get("IMAGE_URL", "https://picsum.photos/1200")
CACHE_SECONDS = int(os.environ.get("CACHE_SECONDS", "600"))

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Todo app</title>
</head>
<body>
  <h1>Todo app</h1>
  <img src="/image" alt="Random image" width="600">
</body>
</html>
"""

download_lock = threading.Lock()


def download_image():
    if not download_lock.acquire(blocking=False):
        return  # 已經有另一個下載在進行
    try:
        os.makedirs(IMAGE_DIR, exist_ok=True)
        tmp = IMAGE_PATH + ".tmp"
        with urllib.request.urlopen(IMAGE_URL, timeout=30) as resp, open(tmp, "wb") as f:
            f.write(resp.read())
        os.replace(tmp, IMAGE_PATH)
        print("Downloaded a new image", flush=True)
    except Exception as e:
        print(f"Image download failed: {e}", flush=True)
    finally:
        download_lock.release()


class Handler(BaseHTTPRequestHandler):
    def send(self, status, content_type, body, no_cache=False):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        if no_cache:
            self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/":
            self.send(200, "text/html; charset=utf-8", HTML.encode("utf-8"))

        elif self.path == "/image":
            if not os.path.exists(IMAGE_PATH):
                download_image()  # 第一次：沒有圖可給，只能等下載完
            if not os.path.exists(IMAGE_PATH):
                self.send(503, "text/plain; charset=utf-8", b"Image not available\n")
                return

            expired = time.time() - os.path.getmtime(IMAGE_PATH) > CACHE_SECONDS
            with open(IMAGE_PATH, "rb") as f:
                body = f.read()
            self.send(200, "image/jpeg", body, no_cache=True)  # 先回傳目前的圖（可能是舊的）

            if expired:
                threading.Thread(target=download_image, daemon=True).start()  # 背景換新圖

        elif self.path == "/shutdown":
            self.send(200, "text/plain; charset=utf-8", b"Shutting down\n")
            print("Shutdown requested", flush=True)
            os._exit(1)

        else:
            self.send(404, "text/plain; charset=utf-8", b"Not found\n")


server = HTTPServer(("0.0.0.0", PORT), Handler)
print(f"Server started in port {PORT}", flush=True)
server.serve_forever()