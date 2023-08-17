from dataclasses import dataclass

import config
from screenshots.logic.helpers.parse_link_type import parse_link_type
from screenshots.logic.screenshooter import Screenshooter


@dataclass
class URLConfig:
    original_url_cleaned: str
    two_layer: bool
    foreground_url: str
    background_url: str
    login_required: bool
    domain: str


def prep_for_screenshots(order: dict) -> dict:
    clean_original_url, domain, two_layer = parse_link_type(url=order.get("link"))

    if not two_layer:
        foreground_url = ""
        background_url = clean_original_url
    else:
        

    login_required = True if domain in config.LOGIN_REQUIRED else False


    return {
        "original_url_cleaned": clean_original_url,
        "two_layer": two_layer,
        "foreground_url": foreground_url,
        "background_url": background_url,
        "login_required": login_required,
        "domain": domain,
    }
