    def login_to_social(self) -> bool:
        for domain in config.LOGIN_REQUIRED:
            chrome_options = Options()
            chrome_options.add_experimental_option(
                "excludeSwitches", ["enable-automation"]
            )
            login_driver = webdriver.Chrome(
                options=chrome_options, service=Service(ChromeDriverManager().install())
            )
            login_driver.implicitly_wait(5)

            website_link = config.SOCIAL_WEBSITES[domain]
            login_driver.get(website_link)

            try:
                self.cookie_manager.add_domain_cookies(domain, login_driver)
                time.sleep(2)
                login_driver.refresh()
            except:
                print(f"No cookies avalable for domain: {domain}")

            if self.login_routines.login_checks[domain](login_driver):
                print(f"Already logged into domain: {domain}")
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