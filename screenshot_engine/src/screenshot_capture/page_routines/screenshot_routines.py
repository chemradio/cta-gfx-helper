from typing import Callable

from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement

from src.helpers.link_parse import parse_link_type

from . import workflows

WORKFLOW_DICT = {
    "facebook": {
        "post": workflows.facebook_post_routine,
        "profile": workflows.facebook_profile_routine,
        "extract_profile": workflows.extract_facebook_profile_url,
    },
    "instagram": {
        "post": workflows.instagram_post_routine,
        "profile": workflows.instagram_profile_routine,
        "extract_profile": workflows.extract_instagram_profile_url,
    },
    "twitter": {
        "post": workflows.twitter_post_routine,
        "profile": workflows.twitter_profile_routine,
        "extract_profile": workflows.extract_twitter_profile_url,
    },
    "telegram": {
        "post": workflows.telegram_post_routine,
        "profile": workflows.telegram_profile_routine,
        "extract_profile": workflows.extract_telegram_profile_url,
    },
    "vk": {
        "post": workflows.vk_post_routine,
        "profile": workflows.vk_profile_routine,
        "extract_profile": workflows.extract_vk_profile_url,
    },
    "scroll": {
        "post": None,
        "profile": workflows.scroll_routine,
        "extract_profile": workflows.extract_scroll_profile_url,
    },
}


def post_workflow(driver: webdriver.Chrome | webdriver.Remote) -> WebElement:
    domain = parse_link_type(driver.current_url).domain

    workflow: Callable | None = WORKFLOW_DICT.get(domain).get("post")

    return workflow(driver=driver)


def profile_workflow(driver: webdriver.Chrome | webdriver.Remote) -> WebElement:
    domain = parse_link_type(driver.current_url).domain

    workflow: Callable = WORKFLOW_DICT.get(domain, WORKFLOW_DICT.get("scroll")).get(
        "profile"
    )

    return workflow(driver=driver)


def extract_profile_url(driver: webdriver.Chrome | webdriver.Remote) -> str:
    domain = parse_link_type(driver.current_url).domain

    workflow: Callable = WORKFLOW_DICT.get(domain, WORKFLOW_DICT.get("scroll")).get(
        "extract_profile"
    )
    print(workflow, flush=True)

    return workflow(driver=driver)
