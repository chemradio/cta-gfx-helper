from selenium import webdriver

from src.helpers.link_parse import DomainName, parse_link_type

from .checkflows.facebook import check_fb_login
from .checkflows.instagram import check_instagram_login
from .checkflows.twitter import check_twitter_login
from .checkflows.vk import check_vk_login


def check_domain_login(driver: webdriver.Chrome | webdriver.Remote) -> bool:
    domain = parse_link_type(driver.current_url).domain

    match domain:
        case "instagram":
            return check_instagram_login(driver)
        case "facebook":
            return check_fb_login(driver)
        case "twitter":
            return check_twitter_login(driver)
        case "vk":
            return check_vk_login(driver)
        case _:
            return None
