from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


def facebook_post_routine(driver: webdriver.Chrome | webdriver.Remote) -> WebElement:
    post = driver.find_element(By.XPATH, "//div[@role='article']")
    # this is for anonymous session. to be deprecated user should always be logged in
    # driver.execute_script(
    #     """el = document.querySelectorAll('[role="feed"]')[0];
    # el.style.width = '500px';"""
    # )
    return post


def facebook_profile_routine(driver: webdriver.Chrome | webdriver.Remote) -> WebElement:
    driver.execute_script("document.body.style.zoom = '1.2'")
    return driver.find_element(By.TAG_NAME, "body")
