import re


def parse_url(url: str) -> str:
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    found_patterns = re.findall(regex, url)
    if not found_patterns:
        raise ValueError("No URL found in the provided string.")

    found_url = found_patterns[0][0]
    if found_url.startswith(('http://', 'https://')):
        return url
    
    return 'https://' + found_url

