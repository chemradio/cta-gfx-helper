from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


def twitter_post_routine(driver: webdriver.Chrome | webdriver.Remote) -> WebElement:
    driver.execute_script("window.scrollTo(0,0)")
    post = driver.find_element(By.XPATH, "//article[@tabindex='-1']")
    return post


def twitter_profile_routine(driver: webdriver.Chrome | webdriver.Remote) -> WebElement:
    driver.execute_script("document.body.style.zoom = '1.2'")
    driver.execute_script(
        """el = document.querySelectorAll('[role="group"]')[0];
    el.parentNode.removeChild(el);"""
    )
    return driver.find_element(By.TAG_NAME, "body")


def extract_twitter_profile_url(driver: webdriver.Chrome | webdriver.Remote) -> str:
    post = driver.find_element(By.TAG_NAME, "article")
    return post.find_element(By.TAG_NAME, "a").get_attribute("href")
