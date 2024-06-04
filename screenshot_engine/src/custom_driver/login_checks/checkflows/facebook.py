from selenium import webdriver
from selenium.webdriver.common.by import By


def check_fb_login(driver: webdriver.Chrome | webdriver.Remote) -> bool:
    try:
        friends_button = driver.find_element(
            By.XPATH, '//a[@href="https://www.facebook.com/friends/"]'
        )
        messenger_button = driver.find_element(
            By.XPATH, '//div[@aria-label="Messenger"]'
        )
        # if it works, we're already logged in
        return True
    except:
        # means we're not logged in
        # continue authentication
        return False
