from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from pathlib import Path


def instagram_post_routine(driver: webdriver.Remote) -> WebElement:
    script_path = Path(__file__).parent.parent / "js_scripts" / "igPost.js"
    with open(script_path, "r") as file:
        script = file.read()
    post = driver.execute_script(script)
    return post


def instagram_profile_routine(
    driver: webdriver.Remote,
) -> WebElement:
    driver.execute_script("document.body.style.zoom = '1'")
    return driver.find_element(By.TAG_NAME, "body")


def extract_instagram_profile_url(driver: webdriver.Remote) -> str:
    post = instagram_post_routine(driver)
    return post.find_element(By.TAG_NAME, "a").get_attribute("href")
