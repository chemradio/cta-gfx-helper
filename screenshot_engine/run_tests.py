from pathlib import Path

from src import main_capture

COOKIE_FILE_PATH = Path.cwd() / "storage" / "cookie_file.json"
REMOTE_DRIVER_URL = "http://localhost:4444/wd/hub"
TARGET_URL = "https://x.com/GeniusGTX/status/1807056930193723595"

result = main_capture(TARGET_URL, REMOTE_DRIVER_URL, COOKIE_FILE_PATH, 2)

for i, of in enumerate(result.operator_output):
    with open(f"./xyz_{i}.png", "wb") as f:
        f.write(of.content.getvalue())
