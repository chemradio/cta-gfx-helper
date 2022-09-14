import time
from engines.screenshots.cookie_manager import CookieManager
from engines.screenshots.login_routines import LoginRoutines
import interlinks
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from engines.screenshots.ad_block.adblock_script_generator import remove_ads_script


class ScreenshotWebdriver:
    def __init__(self, only_for_login: bool = False, mobile: bool = True) -> None:
        self.cookie_manager = CookieManager()
        self.login_routines = LoginRoutines()
        self.dpi_multiplier = interlinks.DPI_MULTIPLIER

        if only_for_login:
            return

        chrome_options = Options()
        # chrome_options.add_argument("--incognito")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.headless = True

        desktop_user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6.1 Safari/605.1.15"
        mobile_user_agent = "userAgent=Mozilla/5.0 (iPhone; CPU iPhone OS 15_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/101.0.4951.44 Mobile/15E148 Safari/604.1"
        user_agent = mobile_user_agent if mobile else desktop_user_agent
        
        device_emulation = {"deviceMetrics": {"width": 1920, "height": 6000,"pixelRatio": self.dpi_multiplier,},
                            "userAgent": user_agent
                            }
        chrome_options.add_experimental_option("mobileEmulation", device_emulation)

        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("-–disable-gpu")

        if interlinks.USE_REMOTE_DRIVER:
            self.driver = webdriver.Remote(interlinks.REMOTE_SCREENSHOT_DRIVER_URL, options=chrome_options)
        else:
            self.driver = webdriver.Chrome(options=chrome_options, service=Service(ChromeDriverManager().install()))

        self.driver.implicitly_wait(5)


    def login_to_social(self) -> bool:
        for domain in interlinks.LOGIN_REQUIRED:
            chrome_options = Options()
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            login_driver = webdriver.Chrome(options=chrome_options, service=Service(ChromeDriverManager().install()))
            login_driver.implicitly_wait(5)

            website_link = interlinks.SOCIAL_WEBSITES[domain]
            login_driver.get(website_link)

            try:
                self.cookie_manager.add_domain_cookies(domain, login_driver)
                time.sleep(2)
                login_driver.refresh()
            except:
                print(f"No cookies avalable for domain: {domain}")

            if self.login_routines.login_checks[domain](login_driver):
                print(f'Already logged into domain: {domain}')
                domain_cookies = login_driver.get_cookies()
                self.cookie_manager.dump_domain_cookies(domain, domain_cookies)
                login_driver.quit()
                continue

            # Give user time to log in to website/social network
            while True:
                try:
                    _ = login_driver.window_handles
                    domain_cookies = login_driver.get_cookies()
                    time.sleep(1)
                except:
                    break

            if domain_cookies:
                self.cookie_manager.dump_domain_cookies(domain, domain_cookies)

            time.sleep(1)
            login_driver.quit()
            time.sleep(2)


    def remove_ads(self) -> None:
        adblock_js = remove_ads_script()
        try:
            self.driver.execute_script(adblock_js)
        except:
            print(f"Failed to remove ads from URL: {self.driver.current_url}")
            pass


