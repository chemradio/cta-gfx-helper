import time

import config
from screenshots.logic.controllers.auth_controller.cookie_manager.cookie_manager import (
    CookieManager,
)
from screenshots.logic.controllers.auth_controller.login_checks import LoginChecker
from screenshots.logic.custom_driver.create_driver import create_driver


def generate_cookies() -> None:
    CookieManager.initialize_cookie_storage()

    for domain in config.LOGIN_REQUIRED:
        driver = create_driver(high_resolution=False)
        driver.implicitly_wait(5)
        website_link = config.SOCIAL_WEBSITES[domain]
        driver.get(website_link)

        try:
            CookieManager.add_cookies_driver(domain, driver)
            time.sleep(2)
            driver.refresh()
        except:
            print(f"No cookies avalable for domain: {domain}")

        if LoginChecker.check_domain_login(driver, domain):
            print(f"Already logged into domain: {domain}")
            domain_cookies = driver.get_cookies()
            CookieManager.dump_domain_cookies(domain, domain_cookies)
            continue

        # Give user time to log in to website/social network
        while True:
            try:
                _ = driver.window_handles
                domain_cookies = driver.get_cookies()
                time.sleep(1)
            except:
                break

        if domain_cookies:
            CookieManager.dump_domain_cookies(domain, domain_cookies)

        time.sleep(1)

        driver.quit()
