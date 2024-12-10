from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from pathlib import Path


def facebook_post_routine(driver: webdriver.Remote) -> WebElement:
    script_path = Path(__file__).parent.parent / "js_scripts" / "fbPost.js"
    with open(script_path, "r") as file:
        script = file.read()
    post = driver.execute_script(script)
    return post


def facebook_profile_routine(driver: webdriver.Remote) -> WebElement:
    driver.execute_script("document.body.style.zoom = '1.2'")
    return driver.find_element(By.TAG_NAME, "body")


def extract_facebook_profile_url(driver: webdriver.Remote) -> str:
    url = driver.current_url
    if "/posts/" in url:
        return url[: url.index("/posts/")]
    else:
        post = facebook_post_routine(driver)
        return post.find_element(By.TAG_NAME, "a").get_attribute("href")
