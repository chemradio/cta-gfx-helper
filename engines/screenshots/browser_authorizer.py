from selenium.webdriver.common.by import By
from selenium import webdriver
import interlinks
from engines.screenshots.cookie_manager import CookieManager
from engines.screenshots.login_routines import LoginRoutines
import time


class BrowserAuthorizer:
    def __init__(self) -> None:
        self.cookie_manager = CookieManager()
        self.login_routines = LoginRoutines()
        pass


    def login_driver_to_domain(self, driver: webdriver.Chrome, domain: str = '') -> bool:
        website_link = interlinks.SOCIAL_WEBSITES[domain]
        driver.get(website_link)
        try:
            self.cookie_manager.add_domain_cookies(domain, driver)
            time.sleep(2)
            driver.refresh()
            if self.login_routines.login_checks[domain](driver):
                print(f'Successfully logged into domain: {domain}')
                domain_cookies = driver.get_cookies()
                self.cookie_manager.dump_domain_cookies(domain, domain_cookies)
                return True
        except:
            print(f"No cookies avalable for domain: {domain}")
            return False
