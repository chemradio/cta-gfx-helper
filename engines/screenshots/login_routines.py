from selenium.webdriver.common.by import By
from selenium import webdriver
import interlinks
import time


class LoginRoutines:
    def __init__(self) -> None:
        self.routines = {'instagram': None}
        self.login_checks = {
            'instagram': self.check_instagram_login,
            'facebook': self.check_fb_login,
            'twitter': self.check_twitter_login,
        }


    def check_instagram_login(self, driver:webdriver.Chrome) -> bool:
        # check if not already logged in
        try:
            search_bar = driver.find_element(By.XPATH, "//input[@aria-label='Search input' and @type='text']")
            profile_button = driver.find_element(By.XPATH, "//span[@role='link']")
            # home_button = driver.find_element(By.XPATH, "//a[@href='/' and @role='link']")
            # likes_button = driver.find_element(By.XPATH, "//a[@href='/accounts/activity']")
            # if it works, we're already logged in
            return True
        except:
            # means we're not logged in
            # continue authentication
            return False


    def check_fb_login(self, driver:webdriver.Chrome) -> bool:
        try:
            friends_button = driver.find_element(By.XPATH, '//a[@href="https://www.facebook.com/friends/"]')
            messenger_button = driver.find_element(By.XPATH, '//div[@aria-label="Messenger"]')
            # if it works, we're already logged in
            return True
        except:
            # means we're not logged in
            # continue authentication
            return False

    
    def check_twitter_login(self, driver: webdriver.Chrome) -> bool:
        try:
            account_menu = driver.find_element(By.XPATH, '//div[@aria-label="Account menu"]')
            dmdrawer = driver.find_element(By.XPATH, '//div[@data-testid="DMDrawer"]')
            notifications = driver.find_element(By.XPATH, '//a[@aria-label="Notifications"]')
            # if it works, we're already logged in
            return True
        except:
            # means we're not logged in
            # continue authentication
            return False


        

    # def instagram_login(self, driver: webdriver.Chrome) -> bool:
    #     if self.check_instagram_login(driver):
    #         return True

    #     try:
    #         switch_accounts_button = driver.find_element(By.XPATH, "//button[contains(., 'Switch accounts')]")
    #         switch_accounts_button.click()
    #         # time.sleep(5)
    #     except:
    #         pass
        
    #     username_field = driver.find_element(By.NAME, "username")
    #     username_field.click()
    #     time.sleep(1)
    #     username_field.send_keys(interlinks.cfg['login_credentials']['instagram']['username'])
    #     time.sleep(1)

    #     password_field = driver.find_element(By.NAME, "password")
    #     password_field.click()
    #     time.sleep(1)
    #     password_field.send_keys(interlinks.cfg['login_credentials']['instagram']['password'])
    #     time.sleep(1)

    #     login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    #     time.sleep(1)
    #     login_button.click()

    #     time.sleep(5)

    #     if not self.check_instagram_login(driver):
    #         return False

    #     return True