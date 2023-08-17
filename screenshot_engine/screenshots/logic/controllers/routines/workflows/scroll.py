from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


def scroll_routine(driver: webdriver.Chrome | webdriver.Remote) -> WebElement:
    driver.execute_script("document.body.style.zoom = '1.0'")
    return driver.find_element(By.TAG_NAME, "body")
