import pickle


import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


# create chrome options and driver objects
chrome_options = Options()
chrome_options.add_argument(f"--force-device-scale-factor={2}")

chrome_options.add_argument(
    f"user-data-dir={os.path.expanduser('~')}/Library/Application Support/Google/Chrome/"
)  # leave out the profile
chrome_options.add_argument("profile-directory=Default")  # enter profile here
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])

driver = webdriver.Chrome(
    options=chrome_options, service=Service(ChromeDriverManager().install())
)


driver.get("http://www.twitter.com")


print(driver.get_cookies())

# pickle.dump( driver.get_cookies() , open("cookies.pkl","wb"))
with open('cookies.py', 'w') as f:
    f.write(str(driver.get_cookies()))

# And later to add them back:

# import pickle
# import selenium.webdriver

# driver = selenium.webdriver.Firefox()
# driver.get("http://www.google.com")
# cookies = pickle.load(open("cookies.pkl", "rb"))
# for cookie in cookies:
#     driver.add_cookie(cookie)
