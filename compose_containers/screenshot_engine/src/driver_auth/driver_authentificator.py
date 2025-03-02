import time
from pathlib import Path

from selenium import webdriver

from .cookie_management import (
    add_cookies_driver,
    dump_domain_cookies,
    get_available_domains_with_cookies,
)
from .login_checks.login_check import check_domain_login

LOGIN_REQUIRED_HOMEPAGES = {
    "facebook": "https://www.facebook.com/",
    "instagram": "https://www.instagram.com/",
    "x": "https://x.com/",
}


def authenticate_driver(
    driver: webdriver.Remote, domain: str, cookie_file: Path, in_place: bool = False
) -> bool:
    if not in_place:
        if domain not in LOGIN_REQUIRED_HOMEPAGES:
            return False
        driver.get(LOGIN_REQUIRED_HOMEPAGES[domain])
    else:
        ...

    try:
        add_cookies_driver(cookie_file, domain, driver)
        time.sleep(2)
        driver.refresh()
        time.sleep(1)
        dump_domain_cookies(cookie_file, domain, driver.get_cookies())

        if not check_domain_login(driver, domain):
            return False
        return True

    except Exception as e:
        print(f"Failed to load cookies for {domain} with error: {e}")
        return False
