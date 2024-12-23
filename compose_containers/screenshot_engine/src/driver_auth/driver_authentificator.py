import time
from pathlib import Path

from selenium import webdriver

from .cookie_management import add_cookies_driver, dump_domain_cookies
from .login_checks.login_check import check_domain_login

LOGIN_REQUIRED_HOMEPAGES = {
    "facebook": "https://www.facebook.com/",
    "instagram": "https://www.instagram.com/",
    "x": "https://x.com/",
}


def authenticate_driver(
    driver: webdriver.Remote, domain: str, cookie_file: Path
) -> bool:
    if domain not in LOGIN_REQUIRED_HOMEPAGES:
        return True

    driver.get(LOGIN_REQUIRED_HOMEPAGES[domain])

    try:
        add_cookies_driver(cookie_file, domain, driver)
        time.sleep(2)
        driver.refresh()
        if not check_domain_login(driver, domain):
            return False

        dump_domain_cookies(cookie_file, domain, driver.get_cookies())
        return True

    except Exception as e:
        print(f"Failed to load cookies for {domain} with error: {e}")
        return False
