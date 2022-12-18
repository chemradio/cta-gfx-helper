import config
from logic.cookie_file_generator import CookieFileGenerator


def main():
    cookie_file_generator = CookieFileGenerator(
        login_required=config.LOGIN_REQUIRED,
        social_websites=config.SOCIAL_WEBSITES,
        cookie_file_path=config.COOKIE_FILE_PATH,
    )

    cookie_file_generator.login_to_social()


if __name__ == "__main__":
    main()
