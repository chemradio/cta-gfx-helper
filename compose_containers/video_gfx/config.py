import os
from pathlib import Path

DISPATCHER_NOIFICATION_URL = f"http://dispatcher:9000"
IS_DOCKER = os.environ.get("IS_DOCKER", False)
STORAGE_PATH = Path.cwd() / "storage"


USE_THREADS = False
USER_PROCESSES = not USE_THREADS
SELENIUM_CONTAINERS_LOCAL = (
    "http://video_gfx_selenium_one:4444/wd/hub",
    "http://video_gfx_selenium_two:4444/wd/hub",
    "http://video_gfx_selenium_three:4444/wd/hub",
)

DEFAULT_ANIMATION_DURATION = 15
DEFAULT_AUDIO_OFFSET = 0.3
VIDEO_BITRATE_BPS = 15_000_000
AUDIO_BITRATE_BPS = 256_000
DEFAULT_FRAMERATE = 25
DEFAULT_VIDEOGFX_TAIL = 2.0

HTML_ASSEMBLIES_FOLDER_PATH = STORAGE_PATH / "html_assemblies"
HTML_TEMPLATES_FOLDER_PATH = Path.cwd() / "src" / "html_composer" / "html_templates"
