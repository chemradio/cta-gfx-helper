from urllib.parse import urlparse, urlunparse
from dataclasses import dataclass


@dataclass
class LinkParse:
    clean_url: str
    domain: str
    two_layer: bool


def _parse_netloc_to_domain(netloc: str) -> str:
    parts = netloc.split(".")
    if "fb.me" in netloc or "facebook" in netloc:
        return "facebook"
    if "instagr" in netloc:
        return "instagram"
    if "t.co" in netloc or "twitter" in netloc:
        return "x"
    if "t.me" in netloc:
        return "telegram"
    return parts[-2]


def _cleanup_netloc(netloc: str) -> str:
    common_prefixes = {"m", "mobile", "www"}  # Add more prefixes if needed
    parsed_url = urlparse(netloc)
    netloc = parsed_url.netloc
    parts = netloc.split(".")
    if parts[0] in common_prefixes:
        parts = parts[1:]
    clean_netloc = ".".join(parts)
    return _cleanup_netloc


def parse_link_type(url: str) -> LinkParse:
    up = urlparse(url)
    netloc = _cleanup_netloc(urlparse(url).netloc)
    domain = _parse_netloc_to_domain(up.netloc)

    if domain in ["facebook", "instagram", "x", "telegram", "vk"]:
        two_layer = True
    else:
        two_layer = False

    return LinkParse(
        clean_url=urlunparse(
            [up.scheme, netloc, up.path, up.params, up.query, up.fragment]
        ),
        domain=domain,
        two_layer=two_layer,
    )
