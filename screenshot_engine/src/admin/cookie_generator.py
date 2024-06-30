import time
from pathlib import Path

from ..custom_driver import create_remote_driver
from ..helpers.driver_auth import HOMEPAGES, LOGIN_REQUIRED, authenticate_driver
from ..helpers.driver_auth.cookie_management import (
    add_cookies_driver,
    dump_domain_cookies,
    initialize_cookie_storage,
)


def generate_cookies(
    remote_driver_url: str,
    cookie_file_path: Path = Path.cwd() / "storage" / "cookie_file.json",
) -> None:
    initialize_cookie_storage(cookie_file_path)

    for domain in LOGIN_REQUIRED:
        driver = create_remote_driver(
            remote_driver_url,
            dpi_multiplier=1,
            vertical_emulation=False,
            headless=False,
        )
        driver.implicitly_wait(5)

        login_success = authenticate_driver(driver, domain, cookie_file_path)

        if login_success:
            print(
                f"Already logged into domain: {domain}, updated cookies successfully dumped to cookie_file."
            )
            continue

        # Give user time to log in to website/social network
        while True:
            try:
                _ = driver.window_handles
                domain_cookies = driver.get_cookies()
                time.sleep(2)
            except:
                break

        if domain_cookies:
            dump_domain_cookies(cookie_file_path, domain, domain_cookies)
            print(f"New cookies for {domain} domain added to cookie_file.")

        driver.quit()
