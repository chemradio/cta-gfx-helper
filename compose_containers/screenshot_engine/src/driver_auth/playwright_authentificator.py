"""Playwright counterpart of ``driver_authentificator.authenticate_driver``.

Same flow as the Selenium path: open the domain homepage, inject the stored
cookies, reload, persist the refreshed cookies, then verify login. The only
extra step is cookie-schema translation - the stored file is always Selenium
format, so cookies are converted on the way into the browser context and
converted back on the way out.
"""

from pathlib import Path

from playwright.sync_api import BrowserContext, Page

from .cookie_management import (
    dump_domain_cookies,
    get_stored_cookies,
    playwright_to_selenium,
    selenium_to_playwright,
)
from .cookie_management.exc import MissingCookies
from .driver_authentificator import LOGIN_REQUIRED_HOMEPAGES
from .login_checks.playwright_login_check import check_domain_login


def _add_stored_cookies(
    context: BrowserContext, domain: str, cookie_file: Path
) -> None:
    """Load this domain's Selenium-format cookies, convert them and add them to
    the Playwright context."""
    domain_cookies = get_stored_cookies(cookie_file).get(domain)
    if not domain_cookies:
        raise MissingCookies(domain=domain)

    playwright_cookies = selenium_to_playwright(domain_cookies)
    try:
        context.add_cookies(playwright_cookies)
        loaded = len(playwright_cookies)
    except Exception as batch_error:
        # one bad cookie rejects the whole batch - retry individually so the
        # good ones still land, mirroring the Selenium per-cookie loop
        print(f"Batch cookie add failed ({batch_error}); retrying one by one")
        loaded = 0
        for cookie in playwright_cookies:
            try:
                context.add_cookies([cookie])
                loaded += 1
            except Exception as cookie_error:
                print(f"Failed cookie {cookie.get('name')!r}: {cookie_error}")

    print(f"Loaded cookies: {loaded}/{len(playwright_cookies)} for {domain}")
    if loaded == 0:
        raise MissingCookies(domain=domain)


def authenticate_page(
    page: Page, context: BrowserContext, domain: str, cookie_file: Path
) -> bool:
    """Authenticate ``page`` for ``domain`` using stored cookies. Returns True
    when the logged-in UI is detected, False otherwise (caller proceeds without
    auth on False, same as the Selenium backend)."""
    if domain not in LOGIN_REQUIRED_HOMEPAGES:
        return False

    try:
        page.goto(LOGIN_REQUIRED_HOMEPAGES[domain])
        _add_stored_cookies(context, domain, cookie_file)
        page.wait_for_timeout(2000)
        page.reload()
        page.wait_for_timeout(1000)

        # persist the refreshed cookies back in canonical Selenium format
        dump_domain_cookies(
            cookie_file, domain, playwright_to_selenium(context.cookies())
        )

        if not check_domain_login(page, domain):
            return False
        return True

    except Exception as e:
        print(f"Failed to load cookies for {domain} with error: {e}")
        return False
