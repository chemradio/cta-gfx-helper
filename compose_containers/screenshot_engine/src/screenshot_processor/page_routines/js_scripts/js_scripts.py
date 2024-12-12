from pathlib import Path


def parse_post(common_script: str) -> str:
    return f"{common_script}\nparsePost();"


def parse_profile(common_script: str) -> str:
    return f"{common_script}\nparseProfile();"


def extract_profile_url(common_script: str) -> str:
    return f"{common_script}\nextractProfileURL();"
