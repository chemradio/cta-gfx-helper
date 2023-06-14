CONTAINER_LIST = [
    "dispatcher",
    "front_svelte",
    "telegram_bot",
    "telegram_sender",
    "db",
    "screenshoter",
    "video_gfx",
    # "video_gfx_server",
    "screenshot_selenium",
    "video_gfx_selenium",
    "storage_unit",
]

CONTAINER_LIST_REQUIRE_VOLUME_MOUNT = [
    # "dispatcher",
    # "front_svelte",
    # "telegram_bot",
    # "telegram_sender",
    # "screenshoter",
    # "video_gfx",
    # "video_gfx_server",
    # "storage_unit",
]

CONTAINER_LIST_REQUIRE_DISPATCHER = [
    "front_svelte",
    "telegram_bot",
    "telegram_sender",
    "screenshoter",
    "video_gfx",
    "storage_unit",
]

CONTAINER_LIST_SELENIUM_MAPPING = {
    "screenshoter": "screenshot_selenium",
    "video_gfx": "video_gfx_selenium",
}

CONTAINER_LIST_BUILD_DEV_FOLDERS = {
    "dispatcher": "./dispatcher_engine",
    "front_svelte": "./front_svelte",
    "telegram_bot": "./bot_engine",
    "telegram_sender": "./sender_engine",
    "screenshoter": "./screenshot_engine",
    "video_gfx": "./video_gfx",
    # "video_gfx_server": "./video_gfx_server",
    "storage_unit": "./storage_unit",
}

CONTAINER_LIST_REQUIRE_CUSTOM_REMOTE_IMAGE = [
    "dispatcher",
    "front_svelte",
    "telegram_bot",
    "telegram_sender",
    "screenshoter",
    "video_gfx",
    # "video_gfx_server",
    "storage_unit",
]

DOCKER_COMPOSE_VERSION = "3.9"
