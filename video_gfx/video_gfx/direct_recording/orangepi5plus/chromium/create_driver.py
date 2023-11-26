from selenium import webdriver
from selenium.webdriver.chromium.options import ChromiumOptions


def create_driver():
    options = ChromiumOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--kiosk")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument("--ignore-gpu-blocklist")
    

    service = webdriver.ChromeService('/usr/lib/chromium-browser/chromedriver')
    return webdriver.Chrome(options=options, service=service)
