import time

from selenium import webdriver

import config
from screenshots.logic.controllers.auth_controller.cookie_manager.cookie_manager import (
    CookieManager,
)
from screenshots.logic.controllers.auth_controller.login_checks import LoginChecker


class BrowserAuthorizer:
    @classmethod
    def check_authorization(cls, driver):
        return LoginChecker.check_domain_login(driver)

    @classmethod
    def login_driver_to_domain(
        cls,
        driver: webdriver.Chrome | webdriver.Remote,
        domain: str,
    ):
        website_link = config.SOCIAL_WEBSITES[domain]
        driver.get(website_link)
        CookieManager.add_domain_cookies(domain=domain, driver=driver)
        time.sleep(2)
        driver.refresh()

        login_success = LoginChecker.check_domain_login(domain=domain, driver=driver)
        if login_success:
            print(f"Successfully logged into domain: {domain}")
            domain_cookies = driver.get_cookies()
            CookieManager.dump_domain_cookies(
                domain=domain, domain_cookies=domain_cookies
            )
            return True
