import html
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

TODOS = [
    "Listen to Yorushika",
    "Listen to Aimer",
    "Listen to nishina",
]

PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Todo app</title>
  <style>
    body {{ font-family: sans-serif; max-width: 700px; margin: 40px auto; padding: 0 16px; color: #333; }}
    h1, h2 {{ text-align: center; }}
    .image {{ display: block; margin: 0 auto 32px; width: 300px; height: 300px; object-fit: cover; border-radius: 8px; }}
    .form {{ display: flex; gap: 8px; margin-bottom: 24px; }}
    .form input {{ flex: 1; padding: 10px; font-size: 16px; border: 2px solid #5cb85c; border-radius: 4px; }}
    .form button {{ padding: 10px 20px; font-size: 16px; background: #5cb85c; color: white; border: none; border-radius: 4px; cursor: pointer; }}
    ul {{ list-style: none; padding: 0; }}
    li {{ padding: 14px; margin-bottom: 8px; background: #f7f7f7; border-left: 4px solid #5cb85c; }}
  </style>
</head>
<body>
  <h1>Todo app</h1>
  <img class="image" src="/image" alt="Random image">

  <div class="form">
    <input type="text" maxlength="140" placeholder="Enter a new todo (max 140 characters)">
    <button type="button">Send</button>
  </div>

  <h2>Todos</h2>
  <ul>
{items}
  </ul>
</body>
</html>
"""


def render_page():
    items = "\n".join(f"    <li>{html.escape(todo)}</li>" for todo in TODOS)
    return PAGE.format(items=items)


download_lock = threading.Lock()


def download_image():
    if not download_lock.acquire(blocking=False):
        return
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
            self.send(200, "text/html; charset=utf-8", render_page().encode("utf-8"))

        elif self.path == "/image":
            if not os.path.exists(IMAGE_PATH):
                download_image()
            if not os.path.exists(IMAGE_PATH):
                self.send(503, "text/plain; charset=utf-8", b"Image not available\n")
                return

            expired = time.time() - os.path.getmtime(IMAGE_PATH) > CACHE_SECONDS
            with open(IMAGE_PATH, "rb") as f:
                body = f.read()
            self.send(200, "image/jpeg", body, no_cache=True)

            if expired:
                threading.Thread(target=download_image, daemon=True).start()

        elif self.path == "/shutdown":
            self.send(200, "text/plain; charset=utf-8", b"Shutting down\n")
            print("Shutdown requested", flush=True)
            os._exit(1)

        else:
            self.send(404, "text/plain; charset=utf-8", b"Not found\n")


server = HTTPServer(("0.0.0.0", PORT), Handler)
print(f"Server started in port {PORT}", flush=True)
server.serve_forever()