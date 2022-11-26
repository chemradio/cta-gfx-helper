def parse_link_type(url: str) -> tuple[str, str]:
    """Gets link type e.g. social media like Facebook. Clean up the url too."""
    clean_url = url

    if "fb.me" in url or "facebook" in url:
        link_type = "facebook"
        if "m.facebook" in url:
            clean_url = "https://" + url[url.index("facebook") :]
    elif "instagr" in url:
        link_type = "instagram"
    elif "/t.co" in url or "twitter" in url:
        link_type = "twitter"
        if "?" in url:
            clean_url = url[: url.index("?")]
    elif "//t.me/" in url:
        link_type = "telegram"
    else:
        link_type = "scroll"

    return link_type, clean_url
