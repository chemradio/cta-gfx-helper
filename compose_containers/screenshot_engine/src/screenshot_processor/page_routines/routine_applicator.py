from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement

from ..types import ScreenshotRole
from .screenshot_routines import post_workflow, profile_workflow


def apply_routine(
    driver: webdriver.Remote, role: ScreenshotRole, domain: str
) -> WebElement:
    if role == ScreenshotRole.POST:
        target_element = post_workflow(driver, domain)
    elif role == ScreenshotRole.FULL_SIZE:
        target_element = profile_workflow(driver, domain)

    return target_element
