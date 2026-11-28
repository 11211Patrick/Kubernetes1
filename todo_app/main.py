import html
import json
import os
import sys
import threading
import time
import urllib.request
from http.server import HTTPServer, BaseHTTPRequestHandler


def require_env(name):
    value = os.environ.get(name)
    if not value:
        sys.exit(f"Missing required environment variable: {name}")
    return value


PORT = int(require_env("PORT"))
TODO_BACKEND_URL = require_env("TODO_BACKEND_URL")
TODO_POST_URL = require_env("TODO_POST_URL")
TODO_MAX_LENGTH = int(require_env("TODO_MAX_LENGTH"))
IMAGE_DIR = require_env("IMAGE_DIR")
IMAGE_URL = require_env("IMAGE_URL")
CACHE_SECONDS = int(require_env("CACHE_SECONDS"))
IMAGE_PATH = os.path.join(IMAGE_DIR, "image.jpg")

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
    .error {{ color: #c0392b; text-align: center; }}
  </style>
</head>
<body>
  <h1>Todo app</h1>
  <img class="image" src="/image" alt="Random image">

  <form class="form" action="{post_url}" method="POST">
    <input type="text" name="todo" maxlength="{max_length}" required placeholder="Enter a new todo (max {max_length} characters)">
    <button type="submit">Send</button>
  </form>

  <h2>Todos</h2>
{todo_section}
</body>
</html>
"""


def fetch_todos():
    with urllib.request.urlopen(TODO_BACKEND_URL, timeout=3) as resp:
        return json.loads(resp.read().decode("utf-8"))


def render_page():
    try:
        todos = fetch_todos()
        items = "\n".join(f"    <li>{html.escape(todo)}</li>" for todo in todos)
        todo_section = f"  <ul>\n{items}\n  </ul>"
    except Exception as e:
        print(f"Failed to fetch todos: {e}", flush=True)
        todo_section = '  <p class="error">Could not load todos.</p>'
    return PAGE.format(
        post_url=html.escape(TODO_POST_URL),
        max_length=TODO_MAX_LENGTH,
        todo_section=todo_section,
    )


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