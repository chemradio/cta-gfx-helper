import os

USE_THREADS = False
USER_PROCESSES = not USE_THREADS

DISPATCHER_NODE_HOSTNAME = os.getenv("dispatcher_name", "dispatcher")
DISPATCHER_NODE_PORT = os.getenv("dispatcher_port", 9000)
DISPATCHER_NODE_URL = f"http://{DISPATCHER_NODE_HOSTNAME}:{DISPATCHER_NODE_PORT}"


ORDERS_ENDPOINT = f"{DISPATCHER_NODE_URL}/intercontainer_orders"


# !!!
SELENIUM_CONTAINERS_LOCAL = (
    "http://video_gfx_selenium_one:4444/wd/hub",
    "http://video_gfx_selenium_two:4444/wd/hub",
    "http://video_gfx_selenium_three:4444/wd/hub",
    # "http://video_gfx_selenium_four:4444/wd/hub",
    # "http://video_gfx_selenium_five:4444/wd/hub",
    # "http://video_gfx_selenium_six:4444/wd/hub",
)

SELENIUM_CONTAINERS_REMOTE = (
    "http://10.0.0.2:4444/wd/hub",
    "http://10.0.0.2:4443/wd/hub",
    "http://10.0.0.2:4442/wd/hub",
    "http://10.0.0.2:4441/wd/hub",
    # "http://video_gfx_selenium_four:4444/wd/hub",
    # "http://video_gfx_selenium_five:4444/wd/hub",
    # "http://video_gfx_selenium_six:4444/wd/hub",
)

USE_REMOTE_DRIVER = True

AUDIO_OFFSET = 0.3

from pathlib import Path

VOLUME_MOUNTPOINT = Path.cwd() / "volume"
HTML_ASSEMBLIES_FOLDER = VOLUME_MOUNTPOINT / "html_assemblies"
HTML_TEMPLATE_FOLDER = Path.cwd() / "video_gfx" / "html_template"

SCREENSHOTS_FOLDER = VOLUME_MOUNTPOINT / "screenshots"
USER_FILES_FOLDER = VOLUME_MOUNTPOINT / "user_files"
STORAGE_UNIT_FOLDER = VOLUME_MOUNTPOINT / "from_storage_unit"

RENDER_OUTPUT_PATH = VOLUME_MOUNTPOINT / "video_exports"

VIDEO_BITRATE_BPS = 15_000_000
AUDIO_BITRATE_BPS = 256_000
AUDIO_OFFSET = 0.3

USE_DOCKER = True
ASSET_SEVER_NAME = os.getenv("video_gfx_name", "video_gfx")
ASSET_SERVER_ACCESS_PORT = os.getenv("video_gfx_port", 9004)
ASSET_SERVER_ACCESS_URL = f"http://{ASSET_SEVER_NAME}:{ASSET_SERVER_ACCESS_PORT}"
ASSET_SERVER_ACCESS_URL_FOR_REMOTES = f"http://10.0.0.1:9004"

STORAGE_UNIT_NAME = os.getenv("storage_unit_name", "storage_unit")
STORAGE_UNIT_PORT = os.getenv("storage_unit_port", 9010)
STORAGE_UNIT_URL = f"http://{STORAGE_UNIT_NAME}:{STORAGE_UNIT_PORT}/file"

DOCKER_PATH_PREFIX = "/usr/src/app"
DEFAULT_ANIMATION_DURATION = 25
