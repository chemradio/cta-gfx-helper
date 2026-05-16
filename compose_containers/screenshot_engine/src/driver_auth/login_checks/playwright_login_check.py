"""Playwright counterpart of ``login_check`` and its ``checkflows/*``.

Same selectors as the Selenium checkflows - just resolved with
``page.query_selector`` instead of ``driver.find_element``. Each check returns
True when the logged-in UI is present.
"""

from playwright.sync_api import Page


def _all_present(page: Page, xpaths: list[str]) -> bool:
    """True only if every XPath matches an element on the page."""
    return all(page.query_selector(f"xpath={xpath}") for xpath in xpaths)


def check_twitter_login(page: Page) -> bool:
    # presence of the compose-post button means we're logged in
    return _all_present(
        page,
        ['//a[@aria-label="Post"]', '//a[@href="/compose/post"]'],
    )


def check_instagram_login(page: Page) -> bool:
    return _all_present(
        page,
        [
            "//span[text()='Profile']",
            "//span[text()='Explore']",
            "//span[text()='Search']",
        ],
    )


def check_fb_login(page: Page) -> bool:
    # mirrors the Selenium checkflow, which short-circuits to True
    return True


def check_vk_login(page: Page) -> None:
    # mirrors the Selenium checkflow stub
    ...


def check_domain_login(page: Page, domain: str) -> bool:
    match domain:
        case "instagram":
            return check_instagram_login(page)
        case "facebook":
            return check_fb_login(page)
        case "twitter":
            return check_twitter_login(page)
        case "vk":
            return check_vk_login(page)
        case _:
            return None
