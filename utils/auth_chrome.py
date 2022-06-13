import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def auth_chrome():
    chrome_options = Options()
    chrome_options.add_argument(f"user-data-dir={os.path.expanduser('~')}/Library/Application Support/Google/Chrome/") #leave out the profile
    chrome_options.add_argument("profile-directory=Default") #enter profile here
    chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
    driver = webdriver.Chrome(
        options=chrome_options,
        service=Service(ChromeDriverManager().install())
    )
    driver.get('http://google.com')

    time.sleep(300)


if __name__ == '__main__':
    auth_chrome()