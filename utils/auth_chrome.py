import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import threading


def auth_chrome():
    chrome_options = Options()
    chrome_options.add_argument(f"user-data-dir={os.path.expanduser('~')}/Library/Application Support/Google/Chrome/") #leave out the profile
    chrome_options.add_argument("profile-directory=Default") #enter profile here
    chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
    driver = webdriver.Chrome(
        options=chrome_options,
        service=Service(ChromeDriverManager().install())
    )
    driver.get('http://facebook.com')

    while True:
        try:
            _ = driver.window_handles
        except:
            break


if __name__ == '__main__':
    auth_chrome()