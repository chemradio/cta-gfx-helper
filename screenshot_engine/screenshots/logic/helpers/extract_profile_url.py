from selenium import webdriver

from screenshots.logic.helpers.parse_link_type import parse_link_type


def extract_profile_url(driver: webdriver.Chrome | webdriver.Remote) -> str:
    """Gets webdriver as a first parameter. Gets current url and tries to extract
    profile url of from a social media post link"""
    clean_url, domain, two_layer = parse_link_type(driver.current_url)

    return ""
