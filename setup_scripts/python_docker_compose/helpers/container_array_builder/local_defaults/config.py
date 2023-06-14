from dataclasses import dataclass


@dataclass
class LocalDefaultConfig:
    DISPATCHER_NAME = "dispatcher"
    DISPATCHER_PORT = 9000
    DISPATCHER_IMAGE = ""
    DISPATCHER_BUILD = "./dispatcher_engine"

    FRONT_SVELTE_NAME = "front_svelte"
    FRONT_SVELTE_PORT = 9009
    FRONT_SVELTE_IMAGE = ""
    FRONT_SVELTE_BUILD = "./front_svelte"

    TELEGRAM_BOT_NAME = "telegram_bot"
    TELEGRAM_BOT_PORT = 9001
    TELEGRAM_BOT_IMAGE = ""
    TELEGRAM_BOT_BUILD = "./bot_engine"

    TELEGRAM_SENDER_NAME = "sender"
    TELEGRAM_SENDER_PORT = 9007
    TELEGRAM_SENDER_IMAGE = ""
    TELEGRAM_SENDER_BUILD = "./sender_engine"

    DB_NAME = "db"
    DB_PORT = ""
    DB_IMAGE = "postgres:15-alpine"
    DB_BUILD = ""

    SCREENSHOTER_NAME = "screenshoter"
    SCREENSHOTER_PORT = 9002
    SCREENSHOTER_IMAGE = ""
    SCREENSHOTER_BUILD = "./screenshot_engine"

    VIDEO_GFX_NAME = "video_gfx"
    VIDEO_GFX_PORT = 9004
    VIDEO_GFX_IMAGE = ""
    VIDEO_GFX_BUILD = "./video_gfx"

    # VIDEO_GFX_SERVER_NAME = "video_gfx_server"
    # VIDEO_GFX_SERVER_PORT = 9006
    # VIDEO_GFX_SERVER_IMAGE = ""
    # VIDEO_GFX_SERVER_BUILD = "./video_gfx_server"

    STORAGE_UNIT_NAME = "storage_unit"
    STORAGE_UNIT_PORT = 9010
    STORAGE_UNIT_IMAGE = ""
    STORAGE_UNIT_BUILD = "./storage_unit"

    SCREENSHOT_SELENIUM_NAME = "screenshot_selenium"
    SCREENSHOT_SELENIUM_PORT = ""
    SCREENSHOT_SELENIUM_IMAGE = "seleniarm/standalone-chromium"
    SCREENSHOT_SELENIUM_BUILD = ""

    VIDEO_GFX_SELENIUM_NAME = "video_gfx_selenium"
    VIDEO_GFX_SELENIUM_PORT = ""
    VIDEO_GFX_SELENIUM_IMAGE = "seleniarm/standalone-chromium"
    VIDEO_GFX_SELENIUM_BUILD = ""
