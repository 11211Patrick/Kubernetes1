import os
import time
import uuid
from datetime import datetime, timezone

FILE_PATH = os.environ.get("FILE_PATH", "/usr/src/app/files/log.txt")

random_string = str(uuid.uuid4())
os.makedirs(os.path.dirname(FILE_PATH), exist_ok=True)

while True:
    ts = datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")
    line = f"{ts}: {random_string}"
    with open(FILE_PATH, "a") as f:
        f.write(line + "\n")
    print(line, flush=True)
    time.sleep(5)