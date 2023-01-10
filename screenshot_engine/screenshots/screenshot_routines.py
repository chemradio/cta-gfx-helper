import time
from typing import Callable
from urllib.parse import urlparse

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

SLEEP_DELAY_1S = 2


def sleeper_decorator(function, sleep_time: int = SLEEP_DELAY_1S):
    def wrapper(*args, **kwargs):
        time.sleep(sleep_time)
        value = function(*args, **kwargs)
        time.sleep(sleep_time)
        return value

    return wrapper


class ScreenshotRoutines:
    def __init__(self) -> None:
        self.workflow = self.ScreenshotWorkflow()
        pass

    class ScreenshotWorkflow:
        def __init__(
            self, post_routine: Callable = None, profile_routine: Callable = None
        ):
            self.post_routine = post_routine
            self.profile_routine = profile_routine

    def create_workflow(self, link_type: str) -> ScreenshotWorkflow:
        self.workflows = {
            "facebook": {
                "post": self.facebook_post_routine,
                "profile": self.facebook_profile_routine,
            },
            "instagram": {
                "post": self.instagram_post_routine,
                "profile": self.instagram_profile_routine,
            },
            "twitter": {
                "post": self.twitter_post_routine,
                "profile": self.twitter_profile_routine,
            },
            "telegram": {
                "post": self.telegram_post_routine,
                "profile": self.telegram_profile_routine,
            },
            "scroll": {
                "post": None,
                "profile": self.scroll_routine,
            },
        }

        return self.ScreenshotWorkflow(
            post_routine=self.workflows[link_type]["post"],
            profile_routine=self.workflows[link_type]["profile"],
        )

    def parse_url(self, url: str) -> tuple[str, str]:
        """Gets link type e.g. social media like Facebook. Clean up url too."""
        clean_url = url

        if "fb.me" in url or "facebook" in url:
            link_type = "facebook"
            if "m.facebook" in url:
                clean_url = "https://" + url[url.index("facebook") :]
        elif "instagr" in url:
            link_type = "instagram"
        elif "/t.co" in url or "twitter" in url:
            link_type = "twitter"
            if "?" in url:
                clean_url = url[: url.index("?")]
        elif "//t.me/" in url:
            link_type = "telegram"
        else:
            link_type = "scroll"

        domain = urlparse(url).netloc
        return link_type, clean_url, domain

    def extract_profile_url(
        self, link_type: str, url: str, driver=None, post=None
    ) -> str:
        if link_type == "facebook":
            if "/posts/" in url:
                link_to_profile = url[: url.index("/posts/")]
            else:
                link_to_profile = post.find_element(By.TAG_NAME, "a").get_attribute(
                    "href"
                )

        elif link_type == "instagram":
            link_to_profile = post.find_element(By.TAG_NAME, "a").get_attribute("href")

        elif link_type == "twitter":
            post = driver.find_element(By.TAG_NAME, "article")
            link_to_profile = post.find_element(By.TAG_NAME, "a").get_attribute("href")

        elif link_type == "telegram":
            try:
                effective_path = url.split("//t.me/")[1]
                link_to_profile = f"https://t.me/s/{effective_path}"
            except:
                link_to_profile = f"https://t.me/"
            # driver.switch_to.frame(post)
            # link_to_profile = post.find_element(By.TAG_NAME, "a").get_attribute("href")

        elif link_type == "scroll":
            link_to_profile = url

        return link_to_profile

    @sleeper_decorator
    def facebook_post_routine(
        self, url: str = None, driver: webdriver.Chrome = None, logged_in: bool = False
    ) -> WebElement:
        # add routine for processing in unlogged state later
        post = driver.find_element(By.XPATH, f"//div[@role='article']")
        if not logged_in:
            driver.execute_script(
                """el = document.querySelectorAll('[role="feed"]')[0];
            el.style.width = '500px';"""
            )
        time.sleep(1)
        return post

    @sleeper_decorator
    def facebook_profile_routine(
        self, url: str = None, driver: webdriver.Chrome = None, logged_in: bool = False
    ) -> None:
        driver.execute_script("document.body.style.zoom = '1.2'")
        return

    @sleeper_decorator
    def instagram_post_routine(
        self, url: str = None, driver: webdriver.Chrome = None, logged_in: bool = False
    ) -> WebElement:
        time.sleep(3)
        # post_role = "presentation" weird... not used later.delete if not needed
        driver.execute_script(
            """element = document.getElementsByTagName("article")[0];
            element.style.border = "0";
            element.style.margin = "0px";"""
        )

        post = driver.find_element(By.TAG_NAME, "article")
        return post

    @sleeper_decorator
    def instagram_profile_routine(
        self, url: str = None, driver: webdriver.Chrome = None, logged_in: bool = False
    ) -> None:
        driver.execute_script("document.body.style.zoom = '1.2'")
        pass

    @sleeper_decorator
    def twitter_post_routine(
        self, url: str = None, driver: webdriver.Chrome = None, logged_in: bool = False
    ) -> WebElement:
        time.sleep(3)

        driver.execute_script("window.scrollTo(0,0)")
        # with open("screenshots/helper_js_scripts/cleanupTwitterPose.js", 'rt') as script_file:
        #     twitter_post_script = script_file.read()
        # driver.execute_script(twitter_post_script)
        post = driver.find_element(By.XPATH, "//article[@tabindex='-1']")

        return post

    @sleeper_decorator
    def twitter_profile_routine(
        self, url: str = None, driver: webdriver.Chrome = None, logged_in: bool = False
    ) -> None:

        # time.sleep(5)
        driver.execute_script("document.body.style.zoom = '1.2'")
        time.sleep(2)
        driver.execute_script(
            """el = document.querySelectorAll('[role="group"]')[0];
        el.parentNode.removeChild(el);"""
        )
        # time.sleep(5)
        # self.driver.execute_script(
        #     f"""
        # var element = document.querySelector('[class="css-1dbjc4n r-12vffkv"]');
        # if (element)
        #     element.parentNode.removeChild(element);
        # """
        # )
        return

    @sleeper_decorator
    def telegram_post_routine(
        self, url: str = None, driver: webdriver.Chrome = None, logged_in: bool = False
    ) -> WebElement:
        driver.execute_script(
            """iframe = document.querySelector("iframe");
            iframe.style.padding = "0px";
            element = iframe.contentWindow.document.querySelector(".tgme_widget_message_bubble");
            element.style.border = "0";
            element.style.margin = "0px";

            bubbleTail = iframe.contentWindow.document.querySelector(".tgme_widget_message_bubble_tail");
            if (bubbleTail)
                bubbleTail.parentNode.removeChild(bubbleTail);

            messageWidget = iframe.contentWindow.document.querySelector(".js-widget_message");
            messageWidget.style.padding = "0px";"""
        )
        driver.execute_script(
            """document.querySelector(".tgme_page_widget_actions").style.visibility = "hidden";"""
        )
        post = driver.find_element(By.TAG_NAME, "iframe")
        return post

    @sleeper_decorator
    def telegram_profile_routine(
        self, url: str = None, driver: webdriver.Chrome = None, logged_in: bool = False
    ) -> None:
        driver.execute_script("window.scrollTo(0, -document.body.scrollHeight)")
        driver.execute_script(
            """loadingElement = document.querySelector(".tme_messages_more js-messages_more");
        if (loadingElement)
            loadingElement.parentNode.removeChild(loadingElement);
        """
        )
        driver.execute_script("document.body.style.zoom = '1.6'")
        pass

    @sleeper_decorator
    def scroll_routine(
        self, url: str = None, driver: webdriver.Chrome = None, logged_in: bool = False
    ) -> None:
        driver.execute_script("document.body.style.zoom = '1.0'")
