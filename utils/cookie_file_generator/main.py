from pathlib import Path

import config
from logic.cookie_file_generator import CookieFileGenerator
from logic.cookie_manager import CookieManager
from logic.login_routines import LoginRoutines


def main():
    cookie_file_generator = CookieFileGenerator(
        login_required=config.LOGIN_REQUIRED,
        social_websites=config.SOCIAL_WEBSITES,
        remote_webdriver_url="http://localhost:4444/wd/hub",
        cookie_manager=CookieManager(config.COOKIE_FILE_PATH),
        login_routines=LoginRoutines(),
    )

    cookie_file_generator.login_to_social()


if __name__ == "__main__":
    main()
