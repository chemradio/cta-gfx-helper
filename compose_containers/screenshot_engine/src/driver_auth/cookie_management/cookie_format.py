"""Translate cookies between the Selenium and Playwright cookie schemas.

The cookie file on disk is always written in **Selenium format** - that is how
the bot captures cookies and how the legacy backend consumes them. The
Playwright backend can't add Selenium-shaped cookies directly: the two APIs
disagree on a couple of fields. This module bridges the gap so the stored file
stays backend-agnostic.

Differences handled:
  * expiry  <-> expires   (Playwright uses ``expires``, Selenium uses ``expiry``)
  * sameSite              (Playwright requires exactly "Strict"/"Lax"/"None";
                           Selenium is looser and may omit it entirely)
  * Playwright needs ``domain``+``path`` (or a ``url``) to be present.
"""

# Playwright only accepts these three sameSite values, capitalised exactly so.
_SAME_SITE = {
    "strict": "Strict",
    "lax": "Lax",
    "none": "None",
    "no_restriction": "None",
    "unspecified": "Lax",
}


def selenium_to_playwright(cookies: list[dict]) -> list[dict]:
    """Convert Selenium-format cookies into the schema ``context.add_cookies``
    expects. Cookies missing a domain are dropped - Playwright would reject the
    whole batch otherwise."""
    converted: list[dict] = []
    for cookie in cookies:
        domain = cookie.get("domain")
        if not domain:
            print(f"Skipping cookie without domain: {cookie.get('name')!r}")
            continue

        playwright_cookie = {
            "name": cookie["name"],
            "value": cookie["value"],
            "domain": domain,
            "path": cookie.get("path", "/"),
            "secure": bool(cookie.get("secure", False)),
            "httpOnly": bool(cookie.get("httpOnly", False)),
            "sameSite": _SAME_SITE.get(
                str(cookie.get("sameSite", "")).lower(), "Lax"
            ),
        }
        # Selenium stores the expiry as an int unix timestamp under `expiry`;
        # a session cookie simply omits it.
        if cookie.get("expiry") is not None:
            playwright_cookie["expires"] = cookie["expiry"]
        converted.append(playwright_cookie)
    return converted


def playwright_to_selenium(cookies: list[dict]) -> list[dict]:
    """Convert Playwright-format cookies (from ``context.cookies()``) back into
    Selenium format so the cookie file on disk stays in its canonical shape."""
    converted: list[dict] = []
    for cookie in cookies:
        selenium_cookie = {
            "name": cookie["name"],
            "value": cookie["value"],
            "domain": cookie.get("domain", ""),
            "path": cookie.get("path", "/"),
            "secure": bool(cookie.get("secure", False)),
            "httpOnly": bool(cookie.get("httpOnly", False)),
        }
        if cookie.get("sameSite"):
            selenium_cookie["sameSite"] = cookie["sameSite"]
        # Playwright returns expires as a float; -1 means a session cookie.
        expires = cookie.get("expires", -1)
        if expires and expires != -1:
            selenium_cookie["expiry"] = int(expires)
        converted.append(selenium_cookie)
    return converted
