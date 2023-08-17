class MissingCookies(Exception):
    def __init__(self, domain):
        self.domain = domain

    def __str__(self):
        return f"No cookies are available for the domain: {self.domain}"
