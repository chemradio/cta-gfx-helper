from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


def vk_post_routine(driver: webdriver.Chrome | webdriver.Remote) -> WebElement:
    driver.execute_script("window.scrollTo(0,0)")
    post = driver.find_element(By.CLASS_NAME, "wall_module")
    return post


def vk_profile_routine(driver: webdriver.Chrome | webdriver.Remote) -> WebElement:
    driver.execute_script("document.body.style.zoom = '1.2'")
    return driver.find_element(By.TAG_NAME, "body")


def extract_vk_profile_url(driver: webdriver.Chrome | webdriver.Remote) -> str:
    post = vk_post_routine(driver)
    return post.find_element(By.TAG_NAME, "a").get_attribute("href")
