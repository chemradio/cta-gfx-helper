from dataclasses import dataclass


@dataclass
class DefaultContainerPorts:
    dispatcher = 9000
    front_svelte = 9009
    telegram_bot = 9001
    telegram_sender = 9007
    screenshoter = 9002
    video_gfx = 9004
    # video_gfx_server = 9006
    storage_unit = 9010
