from pathlib import Path

import config
from logic.cookie_file_generator import CookieFileGenerator
from logic.cookie_manager import CookieManager
from logic.login_routines import LoginRoutines


def copy_cookie_file_to_dev_volume(main_path: Path, dev_path: Path) -> None:
    import shutil

    shutil.copy(main_path, dev_path)


def main():
    cookie_file_generator = CookieFileGenerator(
        login_required=config.LOGIN_REQUIRED,
        social_websites=config.SOCIAL_WEBSITES,
        remote_webdriver_url="http://localhost:4444/wd/hub",
        cookie_manager=CookieManager(config.COOKIE_FILE_PATH),
        login_routines=LoginRoutines(),
    )

    cookie_file_generator.login_to_social()
    if config.COPY_COOKIE_TO_DEV:
        copy_cookie_file_to_dev_volume(
            main_path=config.COOKIE_FILE_PATH, dev_path=config.DEV_COOKIE_FILE_PATH
        )


if __name__ == "__main__":
    main()
