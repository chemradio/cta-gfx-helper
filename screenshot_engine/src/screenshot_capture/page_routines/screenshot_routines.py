from typing import Callable

from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement

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


def post_workflow(driver: webdriver.Remote, domain: str) -> WebElement:
    workflow: Callable | None = WORKFLOW_DICT.get(domain, WORKFLOW_DICT["scroll"]).get(
        "post"
    )
    return workflow(driver=driver)


def profile_workflow(driver: webdriver.Remote, domain: str) -> WebElement:
    workflow: Callable = WORKFLOW_DICT.get(domain, WORKFLOW_DICT["scroll"]).get(
        "profile"
    )
    return workflow(driver=driver)


def extract_profile_url(driver: webdriver.Remote, domain: str) -> str:
    workflow: Callable = WORKFLOW_DICT.get(domain, WORKFLOW_DICT["scroll"]).get(
        "extract_profile"
    )
    return workflow(driver=driver)
