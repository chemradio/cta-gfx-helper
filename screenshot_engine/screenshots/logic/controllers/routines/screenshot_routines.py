import time
from typing import Callable

from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement

from screenshots.logic.controllers.routines.helpers.exceptions import (
    MissingPostWorkflow,
)
from screenshots.logic.controllers.routines.workflows.facebook import (
    facebook_post_routine,
    facebook_profile_routine,
)
from screenshots.logic.controllers.routines.workflows.instagram import (
    instagram_post_routine,
    instagram_profile_routine,
)
from screenshots.logic.controllers.routines.workflows.scroll import scroll_routine
from screenshots.logic.controllers.routines.workflows.telegram import (
    telegram_post_routine,
    telegram_profile_routine,
)
from screenshots.logic.controllers.routines.workflows.twitter import (
    twitter_post_routine,
    twitter_profile_routine,
)
from screenshots.logic.helpers.parse_link_type import parse_link_type


class ScreenshotRoutines:
    workflow_base = {
        "facebook": {
            "post": facebook_post_routine,
            "profile": facebook_profile_routine,
        },
        "instagram": {
            "post": instagram_post_routine,
            "profile": instagram_profile_routine,
        },
        "twitter": {
            "post": twitter_post_routine,
            "profile": twitter_profile_routine,
        },
        "telegram": {
            "post": telegram_post_routine,
            "profile": telegram_profile_routine,
        },
        "scroll": {
            "post": None,
            "profile": scroll_routine,
        },
    }

    @classmethod
    def post_workflow(
        cls,
        url: str,
        driver: webdriver.Chrome | webdriver.Remote,
    ) -> WebElement:
        _, domain_name, _ = parse_link_type(url)

        workflow: Callable | None = cls.workflow_base.get(domain_name).get("post")
        if not workflow:
            raise MissingPostWorkflow(url)

        return workflow(driver=driver)

    @classmethod
    def profile_workflow(
        cls,
        url: str,
        driver: webdriver.Chrome | webdriver.Remote,
    ) -> WebElement:
        _, domain_name, _ = parse_link_type(url)

        workflow: Callable = cls.workflow_base.get(
            domain_name,
            "scroll",
        ).get("profile")

        return workflow(driver=driver)
