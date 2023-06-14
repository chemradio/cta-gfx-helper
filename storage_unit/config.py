import os
from pathlib import Path

DEFAULT_PATH = Path.cwd() / "store"

DISPATCHER_NAME = os.getenv("dispatcher_name", "dispatcher")
DISPATCHER_NODE_PORT = os.getenv("dispatcher_port", 9000)
DISPATCHER_NODE_URL = f"http://{DISPATCHER_NAME}:{DISPATCHER_NODE_PORT}"
