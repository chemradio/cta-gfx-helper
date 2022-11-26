from selenium.webdriver.common.by import By
from selenium import webdriver
import config
import time


class LoginRoutines:
    def __init__(self) -> None:
        self.routines = {"instagram": None}
        self.login_checks = {
            "instagram": self.check_instagram_login,
            "facebook": self.check_fb_login,
            "twitter": self.check_twitter_login,
        }

    def check_instagram_login(self, driver: webdriver.Chrome) -> bool:
        # check if not already logged in
        try:
            search_bar = driver.find_element(
                By.XPATH, "//input[@aria-label='Search input' and @type='text']"
            )
            profile_button = driver.find_element(By.XPATH, "//span[@role='link']")
            # home_button = driver.find_element(By.XPATH, "//a[@href='/' and @role='link']")
            # likes_button = driver.find_element(By.XPATH, "//a[@href='/accounts/activity']")
            # if it works, we're already logged in
            return True
        except:
            # means we're not logged in
            # continue authentication
            return False

    def check_fb_login(self, driver: webdriver.Chrome) -> bool:
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

    def check_twitter_login(self, driver: webdriver.Chrome) -> bool:
        try:
            account_menu = driver.find_element(
                By.XPATH, '//div[@aria-label="Account menu"]'
            )
            dmdrawer = driver.find_element(By.XPATH, '//div[@data-testid="DMDrawer"]')
            notifications = driver.find_element(
                By.XPATH, '//a[@aria-label="Notifications"]'
            )
            # if it works, we're already logged in
            return True
        except:
            # means we're not logged in
            # continue authentication
            return False
