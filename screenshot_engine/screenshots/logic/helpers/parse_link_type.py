from urllib.parse import urlparse


def parse_link_type(url: str) -> tuple[str, str, bool]:
    """Gets link type e.g. social media like Facebook. Cleans up the url.
    Determines the possibility of two-layer screenshots.
    RETURNS: clean url: str, domain name: str, two layer ready: bool"""

    domain = str()
    two_layer = False
    clean_url = url

    if "fb.me" in url or "facebook" in url:
        two_layer = True
        domain = "facebook"
        if "m.facebook" in url:
            clean_url = "https://" + url[url.index("facebook") :]

    elif "instagr" in url:
        two_layer = True
        domain = "instagram"

    elif ("/t.co" in url) or ("twitter" in url) or ("/x.com/" in url):
        two_layer = True
        domain = "twitter"
        if "?" in url:
            clean_url = url[: url.index("?")]

    elif "//t.me/" in url:
        two_layer = True
        domain = "telegram"

    elif "/vk.com/" in url:
        two_layer = True
        domain = "vk"
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
        domain = ""

    return clean_url, domain, two_layer
