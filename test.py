from selenium import webdriver
import time
from engines.screenshots.cookie_manager import CookieManager
from engines.screenshots.login_routines import LoginRoutines
import interlinks
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager



chrome_options = Options()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--disable-web-security")
# chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
# chrome_options.headless = True

driver = webdriver.Chrome(options=chrome_options, service=Service(ChromeDriverManager().install()))

driver.implicitly_wait(5)
driver.get('file:///Users/tim/code/cta-gfx-telegram-bot/assets/html_assemblies/gfx_html_20220905_14-13-36_582160/main.html')

time.sleep(200)
