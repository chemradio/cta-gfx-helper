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


def get_misc_script(script_name: str) -> str:
    script_path = JS_SCRIPTS_PATH / "misc" / f"{script_name}.js"
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


def apply_misc_scripts(driver: webdriver.Remote, scripts: list[str]) -> None:
    if not scripts:
        return

    for script in scripts:
        misc_script = get_misc_script(script)
        if not misc_script:
            continue
        driver.execute_script(misc_script)
