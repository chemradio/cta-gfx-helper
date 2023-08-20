import time
from typing import Callable

from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement

from screenshots.logic.controllers.routines.helpers.exceptions import (
    MissingPostWorkflow,
)
from screenshots.logic.controllers.routines.workflows.facebook import (
    extract_facebook_profile_url,
    facebook_post_routine,
    facebook_profile_routine,
)
from screenshots.logic.controllers.routines.workflows.instagram import (
    extract_instagram_profile_url,
    instagram_post_routine,
    instagram_profile_routine,
)
from screenshots.logic.controllers.routines.workflows.scroll import (
    extract_scroll_profile_url,
    scroll_routine,
)
from screenshots.logic.controllers.routines.workflows.telegram import (
    extract_telegram_profile_url,
    telegram_post_routine,
    telegram_profile_routine,
)
from screenshots.logic.controllers.routines.workflows.twitter import (
    extract_twitter_profile_url,
    twitter_post_routine,
    twitter_profile_routine,
)
from screenshots.logic.helpers.parse_link_type import parse_link_type


class ScreenshotRoutines:
    workflow_base = {
        "facebook": {
            "post": facebook_post_routine,
            "profile": facebook_profile_routine,
            "extract_profile": extract_facebook_profile_url,
        },
        "instagram": {
            "post": instagram_post_routine,
            "profile": instagram_profile_routine,
            "extract_profile": extract_instagram_profile_url,
        },
        "twitter": {
            "post": twitter_post_routine,
            "profile": twitter_profile_routine,
            "extract_profile": extract_twitter_profile_url,
        },
        "telegram": {
            "post": telegram_post_routine,
            "profile": telegram_profile_routine,
            "extract_profile": extract_telegram_profile_url,
        },
        "scroll": {
            "post": None,
            "profile": scroll_routine,
            "extract_profile": extract_scroll_profile_url,
        },
    }

    @classmethod
    def post_workflow(
        cls,
        driver: webdriver.Chrome | webdriver.Remote,
    ) -> WebElement:
        _, domain_name, _ = parse_link_type(driver.current_url)

        workflow: Callable | None = cls.workflow_base.get(domain_name).get("post")
        if not workflow:
            raise MissingPostWorkflow(driver.current_url)

        return workflow(driver=driver)

    @classmethod
    def profile_workflow(
        cls,
        driver: webdriver.Chrome | webdriver.Remote,
    ) -> WebElement:
        _, domain_name, _ = parse_link_type(driver.current_url)

        workflow: Callable = cls.workflow_base.get(
            domain_name, cls.workflow_base.get("scroll")
        ).get("profile")

        return workflow(driver=driver)

    @classmethod
    def extract_profile_url(
        cls,
        driver: webdriver.Chrome | webdriver.Remote,
    ) -> str:
        _, domain_name, _ = parse_link_type(driver.current_url)

        workflow: Callable = cls.workflow_base.get(
            domain_name, cls.workflow_base.get("scroll")
        ).get("extract_profile")

        return workflow(driver=driver)
