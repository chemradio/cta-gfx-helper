from selenium import webdriver
from selenium.webdriver.common.by import By

from screenshots.logic.helpers.parse_link_type import parse_link_type


class LoginChecker:
    @classmethod
    def check_domain_login(
        cls, driver: webdriver.Chrome | webdriver.Remote, domain: str = ""
    ) -> bool:
        if not domain:
            clean_url, domain, _ = parse_link_type(driver.current_url)

        match domain:
            case "instagram":
                return cls.check_instagram_login(driver=driver)
            case "facebook":
                return cls.check_fb_login(driver=driver)
            case "twitter":
                return cls.check_twitter_login(driver=driver)
            case _:
                return None

    @staticmethod
    def check_instagram_login(driver: webdriver.Chrome | webdriver.Remote) -> bool:
        # check if not already logged in
        try:
            profile_button = driver.find_element(By.XPATH, "//span[text()='Profile']")
            explore_button = driver.find_element(By.XPATH, "//span[text()='Explore']")
            search_button = driver.find_element(By.XPATH, "//span[text()='Search']")

            # see_all_recomendations_link = driver.find_element(
            #     By.XPATH, "//a[@href='/explore/people' and @role='link']"
            # )
            # search_bar = driver.find_element(
            #     By.XPATH, "//input[@aria-label='Search input' and @type='text']"
            # )
            # profile_button = driver.find_element(By.XPATH, "//span[@role='link']")
            # home_button = driver.find_element(By.XPATH, "//a[@href='/' and @role='link']")
            # likes_button = driver.find_element(By.XPATH, "//a[@href='/accounts/activity']")
            # if it works, we're already logged in
            return True
        except:
            # means we're not logged in
            # continue authentication
            return False

    @staticmethod
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

    @staticmethod
    def check_twitter_login(driver: webdriver.Chrome | webdriver.Remote) -> bool:
        try:
            account_menu = driver.find_element(
                By.XPATH, '//div[@aria-label="Account menu"]'
            )
            dmdrawer = driver.find_element(By.XPATH, '//div[@data-testid="DMDrawer"]')
            # if it works, we're already logged in
            return True
        except:
            # means we're not logged in
            # continue authentication
            return False
