from dataclasses import dataclass


@dataclass
class DefaultContainerNames:
    dispatcher = "dispatcher"
    front_svelte = "front_svelte"
    telegram_bot = "telegram_bot"
    telegram_sender = "sender"
    db = "db"
    screenshoter = "screenshoter"
    video_gfx = "video_gfx"
    video_gfx_server = "video_gfx_server"
    screenshot_selenium = "screenshot_selenium"
    video_gfx_selenium = "video_gfx_selenium"
