import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


def scroll_routine(driver: webdriver.Chrome | webdriver.Remote) -> WebElement:
    driver.execute_script("document.body.style.zoom = '1.0'")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(1)
    driver.execute_script("window.scrollTo(0, -document.body.scrollHeight)")
    return driver.find_element(By.TAG_NAME, "body")


def extract_scroll_profile_url(driver: webdriver.Chrome | webdriver.Remote) -> str:
    """Temporary. Should figure out how to remove this."""
    return driver.current_url
