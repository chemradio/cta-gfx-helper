import time
from pathlib import Path

from selenium.webdriver import Remote

from ..adblocker import adblocking
from ..cookie_manager import CookieManager
from ..login_checks import check_domain_login
from .chrome_opts import _generate_chrome_options


class ScreenshotRemoteDriver(Remote):
    def __init__(self, remote_screenshor_url: str, cookie_file_path: str | Path):
        super().__init__(
            command_executor=remote_screenshor_url, options=_generate_chrome_options()
        )
        self.implicitly_wait(5)
        self.cookie_manager = CookieManager(cookie_file_path)

    def remove_ads(self):
        return adblocking.remove_ads(self)

    def check_authentication(self, domain: str | None = None):
        return check_domain_login(self, domain)

    def login_driver_to_domain(self, domain: str):
        SOCIAL_WEBSITES = {
            "facebook": "https://facebook.com",
            "twitter": "https://twitter.com",
            "instagram": "https://instagram.com",
            "vk": "https://vk.com",
        }
        website_link = SOCIAL_WEBSITES[domain]
        self.get(website_link)
        self.cookie_manager.add_cookies_driver(domain=domain, driver=self)
        time.sleep(2)
        self.refresh()

        login_success = self.check_authentication(domain=domain)
        if login_success:
            print(f"Successfully logged into domain: {domain}")
            domain_cookies = self.get_cookies()
            self.cookie_manager.dump_domain_cookies(
                domain=domain, domain_cookies=domain_cookies
            )
            return True
