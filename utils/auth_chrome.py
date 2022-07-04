import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def auth_chrome():
    chrome_options = Options()
    # chrome_options.add_argument(f"user-data-dir={os.path.expanduser('~')}/Library/Application Support/Google/Chrome/") #leave out the profile
    # chrome_options.add_argument("profile-directory=Default") #enter profile here
    chrome_options.add_argument("--incognito")
    chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
    driver = webdriver.Chrome(
        options=chrome_options,
        service=Service(ChromeDriverManager().install())
    )
    driver.get('https://instagram.com')

    # time.sleep(20)
    # cookies = driver.get_cookies()

    while True:
        try:
            _ = driver.window_handles
            time.sleep(1)
        except:
            break


def cookie_test_2():
    chrome_options = Options()
    # chrome_options.add_argument(f"user-data-dir={os.path.expanduser('~')}/Library/Application Support/Google/Chrome/") #leave out the profile
    # chrome_options.add_argument("profile-directory=Default") #enter profile here
    chrome_options.add_argument("--incognito")
    chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
    driver = webdriver.Chrome(
        options=chrome_options,
        service=Service(ChromeDriverManager().install())
    )
    driver.get('https://instagram.com')
    from ck import ck as cookies

    for cookie in cookies:
        try:
            driver.add_cookie(cookie)
        except:
            print('failed to load cookie')



    time.sleep(2)
    driver.get('https://instagram.com')
    time.sleep(40)



if __name__ == '__main__':
    # auth_chrome()
    cookie_test_2()