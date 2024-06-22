import json
from pathlib import Path

from selenium import webdriver

from .exc import CookieLoadException, MissingCookies


def initialize_cookie_storage(cookie_file: Path) -> None:
    """Create cookie file json if does not exist already."""
    if not cookie_file.exists():
        with open(cookie_file, "w+") as cookie_file:
            json.dump({"domain_name": [{}]}, cookie_file)


def get_stored_cookies(cookie_file: Path) -> dict[list[dict]]:
    """Read all cookies from stored cookie file."""
    cookies = dict()
    with open(cookie_file, "r") as c_file:
        cookies = json.load(c_file)
    return cookies


def dump_domain_cookies(
    cookie_file: Path, domain: str, domain_cookies: list[dict]
) -> None:
    """Save specific domain cookies to storage."""
    stored_cookies = get_stored_cookies(cookie_file)
    stored_cookies[domain] = domain_cookies
    with open(cookie_file, "w") as c_file:
        json.dump(stored_cookies, c_file)


def add_cookies_driver(
    cookie_file: Path, domain: str, driver: webdriver.Chrome | webdriver.Remote
) -> None:
    """Add specific domain cookies to webdriver."""
    domain_cookies = get_stored_cookies(cookie_file).get(domain)
    if not domain_cookies:
        raise MissingCookies(domain=domain)

    good_cookies, failed_cookies = 0, 0
    for cookie in domain_cookies:
        try:
            driver.add_cookie(cookie)
            good_cookies += 1
        except Exception as e:
            print(f"Failed to load cookie: {cookie} with error: {e[:10]}")
            failed_cookies += 1

    print(f"Successfully loaded cookies: {good_cookies}/{len(domain_cookies)}")
    print(f"Failed cookies: {failed_cookies}/{len(domain_cookies)}")

    if good_cookies == 0:
        raise CookieLoadException(domain=domain, failed_cookies=failed_cookies)
