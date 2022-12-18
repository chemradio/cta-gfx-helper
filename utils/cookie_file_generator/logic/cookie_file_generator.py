import time
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from logic.cookie_manager import CookieManager
from logic.login_routines import LoginRoutines


class CookieFileGenerator:
    def __init__(
        self,
        login_required: tuple = tuple(),
        social_websites: dict = dict(),
        cookie_file_path: Path = Path(),
    ) -> None:
        self.cookie_manager = CookieManager(cookie_file_path)
        self.login_routines = LoginRoutines()

        self.login_required = login_required
        self.social_websites = social_websites
        self.chrome_options = Options()
        self.chrome_options.add_experimental_option(
            "excludeSwitches", ["enable-automation"]
        )

    def login_to_social(self) -> bool:
        for domain in self.login_required:
            self.driver = webdriver.Chrome(
                options=self.chrome_options,
                service=Service(ChromeDriverManager().install()),
            )
            self.driver.implicitly_wait(5)
            website_link = self.social_websites.get(domain)
            if not website_link:
                print(f"Could not load a website: {domain}")

            self.driver.get(website_link)

            # add pre-existing cookies
            try:
                self.cookie_manager.add_domain_cookies(domain, self.driver)
                time.sleep(2)
                self.driver.refresh()
            except:
                print(f"No cookies avalable for domain: {domain}")

            # check if user is successfully logged in using pre-existing cookies &
            # dump new cookies
            if self.login_routines.login_checks[domain](self.driver):
                print(f"Already logged into domain: {domain}")
                domain_cookies = self.driver.get_cookies()
                self.cookie_manager.dump_domain_cookies(domain, domain_cookies)
                self.driver.quit()
                continue

            # Give user infinite time to log in to website/social network
            while True:
                try:
                    # check if user has closed the window after logging in
                    _ = self.driver.window_handles
                    domain_cookies = self.driver.get_cookies()
                    time.sleep(1)
                except:
                    break

            if domain_cookies:
                self.cookie_manager.dump_domain_cookies(domain, domain_cookies)

            time.sleep(1)
            self.driver.quit()
            time.sleep(1)
