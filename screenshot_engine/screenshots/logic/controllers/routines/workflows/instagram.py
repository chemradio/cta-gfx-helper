from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


def instagram_post_routine(driver: webdriver.Chrome | webdriver.Remote) -> WebElement:
    # post_role = "presentation" weird... not used later.delete if not needed
    driver.execute_script(
        """element = document.getElementsByTagName("article")[0];
        element.style.border = "0";
        element.style.margin = "0px";"""
    )

    post = driver.find_element(By.TAG_NAME, "article")
    return post


def instagram_profile_routine(
    driver: webdriver.Chrome | webdriver.Remote,
) -> WebElement:
    driver.execute_script("document.body.style.zoom = '1.2'")
    return driver.find_element(By.TAG_NAME, "body")


def extract_instagram_profile_url(driver: webdriver.Chrome | webdriver.Remote) -> str:
    post = instagram_post_routine(driver)
    return post.find_element(By.TAG_NAME, "a").get_attribute("href")
