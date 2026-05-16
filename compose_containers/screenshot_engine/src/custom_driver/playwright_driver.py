"""Playwright counterpart of ``screenshot_driver.create_remote_driver``.

The legacy backend talks to a remote Selenium node and emulates the capture
device through Chrome's ``mobileEmulation`` experimental option. This backend
launches headless Chromium in-container and reproduces that emulation through
the **same underlying CDP command** (``Emulation.setDeviceMetricsOverride``) -
so the proven, reliable device-metrics behaviour is preserved, only the
browser transport changes.

``playwright_page`` yields ``(page, context, cdp_session)``. The CDP session is
reused by ``capture_screenshot_playwright`` for ``Page.captureScreenshot``.

Used when ``config.SCREENSHOT_BACKEND == "playwright"``.
"""

from contextlib import contextmanager

from playwright.sync_api import sync_playwright

from .driver_options.user_agent import UserAgent

# Matches the deviceMetrics block in driver_options/chrome_opts.py so the
# playwright backend renders pages at exactly the same emulated resolution.
EMULATED_WIDTH = 1920
EMULATED_HEIGHT = 5760


@contextmanager
def playwright_page(
    dpi_multiplier: int | float,
    user_agent: str = UserAgent.MAC_CHROME,
    vertical_emulation: bool = True,
    headless: bool = True,
):
    """Launch headless Chromium and yield ``(page, context, cdp_session)`` with
    CDP device emulation applied. Everything is torn down on exit."""
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            headless=headless,
            args=[
                "--no-sandbox",
                "--disable-gpu",
                # plain containers have a tiny /dev/shm; without this Chromium
                # can hang or crash mid-render
                "--disable-dev-shm-usage",
                "--disable-notifications",
                "--ignore-certificate-errors",
            ],
        )
        # no_viewport hands all sizing control to the CDP override below,
        # so Playwright's own viewport logic never fights the emulation.
        context = browser.new_context(user_agent=user_agent, no_viewport=True)
        page = context.new_page()

        cdp_session = context.new_cdp_session(page)
        if vertical_emulation:
            # The exact CDP command Chrome's mobileEmulation option issues
            # internally - applied here explicitly to keep the emulation that
            # "proved most reliable" identical under the new backend.
            cdp_session.send(
                "Emulation.setDeviceMetricsOverride",
                {
                    "width": EMULATED_WIDTH,
                    "height": EMULATED_HEIGHT,
                    "deviceScaleFactor": dpi_multiplier,
                    "mobile": True,
                },
            )

        try:
            yield page, context, cdp_session
        finally:
            context.close()
            browser.close()
