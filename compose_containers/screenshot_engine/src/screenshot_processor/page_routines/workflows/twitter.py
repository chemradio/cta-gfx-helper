from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from pathlib import Path


def twitter_post_routine(driver: webdriver.Remote) -> WebElement:
    script_path = Path(__file__).parent.parent / "js_scripts" / "xPost.js"
    with open(script_path, "r") as file:
        script = file.read()
    post = driver.execute_script(script)
    return post


def twitter_profile_routine(driver: webdriver.Remote) -> WebElement:
    driver.execute_script("document.body.style.zoom = '1.2'")
    driver.execute_script(
        """el = document.querySelectorAll('[role="group"]')[0];
    el.parentNode.removeChild(el);"""
    )
    return driver.find_element(By.TAG_NAME, "body")


def extract_twitter_profile_url(driver: webdriver.Remote) -> str:
    post = driver.find_element(By.TAG_NAME, "article")
    return post.find_element(By.TAG_NAME, "a").get_attribute("href")
