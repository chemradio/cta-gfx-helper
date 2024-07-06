import os
from pathlib import Path

DISPATCHER_NOIFICATION_URL = f"http://dispatcher:9000"
IS_DOCKER = os.environ.get("IS_DOCKER", False)
STORAGE_PATH = Path.cwd() / "storage"

USE_THREADS = False
USER_PROCESSES = not USE_THREADS

# !!!
SELENIUM_CONTAINERS_LOCAL = (
    "http://video_gfx_selenium_one:4444/wd/hub",
    "http://video_gfx_selenium_two:4444/wd/hub",
    "http://video_gfx_selenium_three:4444/wd/hub",
    # "http://video_gfx_selenium_four:4444/wd/hub",
    # "http://video_gfx_selenium_five:4444/wd/hub",
    # "http://video_gfx_selenium_six:4444/wd/hub",
)


DEFAULT_ANIMATION_DURATION = 25
AUDIO_OFFSET = 0.3
VIDEO_BITRATE_BPS = 15_000_000
AUDIO_BITRATE_BPS = 256_000
AUDIO_OFFSET = 0.3


HTML_ASSEMBLIES_FOLDER = VOLUME_MOUNTPOINT / "html_assemblies"
HTML_TEMPLATE_FOLDER = Path.cwd() / "video_gfx" / "html_template"

SCREENSHOTS_FOLDER = VOLUME_MOUNTPOINT / "screenshots"
USER_FILES_FOLDER = VOLUME_MOUNTPOINT / "user_files"
RENDER_OUTPUT_PATH = VOLUME_MOUNTPOINT / "video_exports"
