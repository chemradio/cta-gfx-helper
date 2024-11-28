from urllib.parse import urlparse

from .domain_enum import DomainName
from .link_parser_class import LinkParse


def parse_link_type(url: str) -> LinkParse:
    """Gets link type e.g. social media like Facebook. Cleans up the url.
    Determines the possibility of two-layer screenshots.
    RETURNS: clean url: str, domain name: str, two layer ready: bool"""

    clean_url = url
    domain = str()
    two_layer = False

    if "fb.me" in url or "facebook" in url:
        two_layer = True
        domain = DomainName.FACEBOOK
        if "m.facebook" in url:
            clean_url = "https://" + url[url.index("facebook") :]

    elif "instagr" in url:
        two_layer = True
        domain = DomainName.INSTAGRAM

    elif ("/t.co" in url) or ("twitter" in url) or ("/x.com/" in url):
        two_layer = True
        domain = DomainName.TWITTER
        if "?" in url:
            clean_url = url[: url.index("?")]

    elif "//t.me/" in url:
        two_layer = True
        domain = DomainName.TELEGRAM

    elif "/vk.com/" in url:
        two_layer = True
        domain = DomainName.VK
        clean_url = url

        up = urlparse(url)
        if up.path.startswith("/wall"):
            pass
        elif up.query:
            usable_queries = [
                query for query in up.query.split("&") if query.startswith("w=wall")
            ]
            query = usable_queries[0] if usable_queries else None
            if query:
                clean_url = f"https://vk.com/{query[2:]}"

    else:
        two_layer = False
        domain = DomainName.OTHER

    return LinkParse(
        clean_url=clean_url,
        domain=domain,
        two_layer=two_layer,
    )
