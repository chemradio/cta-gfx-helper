class CookieLoadException(Exception):
    def __init__(self, domain: str, failed_cookies: int):
        self.domain = domain
        self.failed_cookies = failed_cookies

    def __str__(self):
        return f"Failed to load {self.failed_cookies} cookies for domain {self.domain}"
