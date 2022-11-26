from screenshots.screenshot_webdriver import ScreenshotWebdriver

login_driver = ScreenshotWebdriver(only_for_login=True)
login_driver.login_to_social()
