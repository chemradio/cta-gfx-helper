from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from pathlib import Path


def telegram_post_routine(driver: webdriver.Remote) -> WebElement:
    script_path = Path(__file__).parent.parent / "js_scripts" / "telegramPost.js"
    with open(script_path, "r") as file:
        script = file.read()
    post = driver.execute_script(script)
    return post


def telegram_profile_routine(driver: webdriver.Remote) -> WebElement:
    driver.execute_script("window.scrollTo(0, -document.body.scrollHeight)")
    driver.execute_script(
        """loadingElement = document.querySelector(".tme_messages_more js-messages_more");
    if (loadingElement)
        loadingElement.parentNode.removeChild(loadingElement);
    """
    )
    driver.execute_script("document.body.style.zoom = '1.6'")
    return driver.find_element(By.TAG_NAME, "body")


def extract_telegram_profile_url(driver: webdriver.Remote) -> str:
    try:
        effective_path = driver.current_url.split("//t.me/")[1]
        return f"https://t.me/s/{effective_path}"
    except:
        return f"https://t.me/"
