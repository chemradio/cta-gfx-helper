"""Playwright counterpart of ``routine_applicator``.

Same per-domain ``js_scripts/<domain>/common.js`` files, same misc scripts -
only the execution differs. Selenium ran them through ``execute_async_script``
with an ``arguments[...]`` callback; Playwright's ``evaluate_handle`` awaits the
returned promise directly, which is both simpler and avoids serialising DOM
nodes back to Python.

``parsePost`` / ``parseProfile`` resolve to a DOM element -> returned as an
``ElementHandle``. ``extractProfileURL`` resolves to a string.
"""

from playwright.sync_api import ElementHandle, Page

from .routine_applicator import get_common_script, get_misc_script


def _run_routine_handle(
    page: Page, common_script: str, routine_call: str
) -> ElementHandle | None:
    """Run ``common.js`` then ``routine_call`` (e.g. ``parsePost()``) and return
    the DOM element it resolves to as an ElementHandle, or None."""
    handle = page.evaluate_handle(
        f"async () => {{ {common_script}\n return await {routine_call}; }}"
    )
    return handle.as_element()


def apply_post_routine(page: Page, domain: str) -> ElementHandle | None:
    common_script = get_common_script(domain)
    if not common_script:
        return page.query_selector("body")
    return _run_routine_handle(page, common_script, "parsePost()")


def apply_profile_routine(page: Page, domain: str) -> ElementHandle | None:
    common_script = get_common_script(domain)
    if not common_script:
        return page.query_selector("body")
    return _run_routine_handle(page, common_script, "parseProfile()")


def extract_profile_url(page: Page, domain: str) -> str:
    common_script = get_common_script(domain)
    if not common_script:
        return ""
    return page.evaluate(
        f"async () => {{ {common_script}\n return await extractProfileURL(); }}"
    )


def apply_misc_scripts(page: Page, scripts: list[str]) -> None:
    if not scripts:
        return

    for script in scripts:
        misc_script = get_misc_script(script)
        if not misc_script:
            continue
        # wrapped in a function body so statement-style scripts (and any
        # top-level `return`) run the same way they did under execute_script
        page.evaluate(f"() => {{ {misc_script} }}")
