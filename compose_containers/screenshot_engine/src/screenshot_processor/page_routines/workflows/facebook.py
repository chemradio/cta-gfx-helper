from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from pathlib import Path

from ..js_scripts.js_scripts import parse_post, parse_profile, extract_profile_url

with open(
    Path(__file__).parent.parent / "js_scripts" / "facebook" / "common.js", "r"
) as file:
    FACEBOOK_COMMON_SCRIPT = file.read()


def facebook_post_routine(driver: webdriver.Remote) -> WebElement:
    post = driver.execute_script(parse_post(FACEBOOK_COMMON_SCRIPT))
    if not post:
        raise Exception("Post/VideoPost not found")
    return post


def facebook_profile_routine(driver: webdriver.Remote) -> WebElement:
    body = driver.execute_script(parse_profile(FACEBOOK_COMMON_SCRIPT))
    return body


def extract_facebook_profile_url(driver: webdriver.Remote) -> str:
    return extract_facebook_profile_url(FACEBOOK_COMMON_SCRIPT)
