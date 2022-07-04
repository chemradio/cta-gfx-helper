from distutils.command.clean import clean
import os
import time
from typing import Any
from engines.screenshots.cookie_manager import CookieManager
from engines.screenshots.login_routines import LoginRoutines
import interlinks
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class ScreenshotWebdriver:
    def __init__(self) -> None:
        self.dpi_multiplier = interlinks.DPI_MULTIPLIER
        chrome_options = Options()
        # chrome_options.add_argument("--incognito")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        device_emulation = {"deviceMetrics": {"width": 1920, "height": 6000,"pixelRatio": self.dpi_multiplier,},
                            # "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) \
                            #     AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19"
                            }
        chrome_options.add_experimental_option("mobileEmulation", device_emulation)

        """Don't use four lines below."""
        # chrome_options.add_argument(f"user-data-dir={os.path.expanduser('~')}/Library/Application Support/Google/Chrome/")
        # chrome_options.add_argument("profile-directory=Default")
        # chrome_options.headless = True
        # chrome_options.add_argument(f"--force-device-scale-factor={dpi_multiplier}")

        self.driver = webdriver.Chrome(options=chrome_options, service=Service(ChromeDriverManager().install()))
        self.driver.implicitly_wait(5)
        self.cookie_manager = CookieManager()
        self.login_routines = LoginRoutines()


    def login_to_social(self, specific_domain: str = '') -> bool:
        for domain in interlinks.LOGIN_REQUIRED:
            if specific_domain and domain != specific_domain:
                continue
                 
            website_link = interlinks.SOCIAL_WEBSITES[domain]
            self.driver.get(website_link)

            try:
                self.cookie_manager.add_domain_cookies(domain, self.driver)
                time.sleep(2)
                self.driver.refresh()
            except:
                print(f"No cookies avalable for domain: {domain}")

            if self.login_routines.login_checks[domain](self.driver):
                print(f'Already logged into domain: {domain}')
                return True

            # Give user time to log in to website/social network
            while True:
                try:
                    _ = self.driver.window_handles
                    domain_cookies = self.driver.get_cookies()
                    time.sleep(1)
                except:
                    break

            if domain_cookies:
                self.cookie_manager.dump_domain_cookies(domain, domain_cookies)


    def super_get(self, url: str, link_type: str, dump: bool = True) -> None:
        # without cookies version
        self.login_to_social()
        time.sleep(2)
        self.driver.get(url)
        return

        # cookies version
        """Get url but parse stored cookies"""
        self.add_stored_cookies(domain=link_type)
        time.sleep(0)
        self.driver.get(url)
        self.add_stored_cookies(domain=link_type)
        self.driver.refresh()
        time.sleep(1)
        time.sleep(1)
        time.sleep(10)
        if dump:
            self.dump_domain_cookies(link_type)
        time.sleep(1)
        return
