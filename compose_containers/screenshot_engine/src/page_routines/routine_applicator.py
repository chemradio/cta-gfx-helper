from pathlib import Path
from selenium.webdriver.remote.webelement import WebElement
from selenium import webdriver
from selenium.webdriver.common.by import By


JS_SCRIPTS_PATH = Path(__file__).parent / "js_scripts"


def get_common_script(domain: str) -> str:
    script_path = JS_SCRIPTS_PATH / domain / "common.js"
    if not script_path.exists():
        return ""
    with open(script_path, "r") as file:
        return file.read()


def apply_post_routine(driver: webdriver.Remote, domain: str) -> WebElement:
    common_script = get_common_script(domain)
    if not common_script:
        return driver.find_element(By.TAG_NAME, "body")
    return driver.execute_async_script(
        common_script
        + "\n"
        + """const callback = arguments[arguments.length - 1];
parsePost().then(callback);"""
    )


def apply_profile_routine(driver: webdriver.Remote, domain: str) -> WebElement:
    common_script = get_common_script(domain)
    if not common_script:
        return driver.find_element(By.TAG_NAME, "body")
    return driver.execute_async_script(
        common_script
        + "\n"
        + """const callback = arguments[arguments.length - 1];
parseProfile().then(callback);"""
    )


def extract_profile_url(driver: webdriver.Remote, domain: str) -> str:
    common_script = get_common_script(domain)
    if not common_script:
        return ""
    return driver.execute_async_script(
        common_script
        + "\n"
        + """const callback = arguments[arguments.length - 1];
extractProfileURL().then(callback);"""
    )
