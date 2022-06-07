import interlinks
import time
import secrets
import threading
import base64
import sys
import os
from engines.telegram_bot import bot
from io import BytesIO
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from database.db import db_handler
from engines.video_gfx_engines import render_video_orders
from engines.sender_engine import send_ready_orders
from telegram import ReplyKeyboardRemove




import logging

logger_screenshot = logging.getLogger(__name__)
logger_screenshot.setLevel(logging.DEBUG)
logging_screenshot_formatter = logging.Formatter("%(asctime)s: %(name)s: %(message)s")
logging_screenshot_file_handler = logging.FileHandler(f"./logs/{__name__}.log", mode='w+')
logging_screenshot_file_handler.setLevel(logging.DEBUG)
logging_screenshot_file_handler.setFormatter(logging_screenshot_formatter)
logging_screenshot_stream_handler = logging.StreamHandler()
logging_screenshot_stream_handler.setFormatter(logging_screenshot_formatter)
logger_screenshot.addHandler(logging_screenshot_file_handler)
# logger_screenshot.addHandler(logging_screenshot_stream_handler)



dpi_multiplier = 2.0
node_screenshot_offset = [10, 0]

def capture_screenshot(url):
    logger_screenshot.debug(f"Capturing screenshots from this URL: {url}")
    # generate file names
    background_name = f"01_BG_{secrets.token_hex(8)}.png"
    foreground_name = f"02_FG_{secrets.token_hex(8)}.png"

    # define website type
    if "fb.me" in url or "facebook" in url:
        link_type = "facebook"
        post_role = "article"
    elif "instagr" in url:
        link_type = "instagram"
        post_role = "presentation"
    elif "/t.co" in url or "twitter" in url:
        link_type = "twitter"
        post_role = "article"
    elif "//t.me/" in url:
        link_type = "telegram"
    else:
        link_type = "scroll"

    logger_screenshot.debug(f"Screenshot link type: {link_type}")

    # create chrome options and driver objects
    chrome_options = Options()
    chrome_options.add_argument(f"--force-device-scale-factor={dpi_multiplier}")
    
    chrome_options.add_argument(f"user-data-dir={os.path.expanduser('~')}/Library/Application Support/Google/Chrome/") #leave out the profile
    chrome_options.add_argument("profile-directory=Default") #enter profile here
    chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
    # chrome_options.headless = True


    driver = webdriver.Chrome(
        options=chrome_options,
        service=Service(ChromeDriverManager().install())
    )

    # previous code containing executable
    # driver = webdriver.Chrome(
    #     options=chrome_options,
    #     executable_path=os.path.join(
    #         interlinks.chrome_drivers, "chromedriver_mac64_100.0.4896.60/chromedriver"
    #     ),
    # )

    is_two_layer = False

    # fb capture
    if link_type == "facebook":
        if "m.facebook" in url:
            url = "https://" + url[url.index("facebook") :]
        driver.get(url)
        time.sleep(2)

        # get post screenshot
        try:
            time.sleep(5)
            post = driver.find_element_by_xpath(f"//div[@role='{post_role}']")
            is_two_layer = True
            capture_post_screenshot(post, foreground_name, driver)

            # get profile link and capture profile page
            if "/posts/" in url:
                link_to_profile = url[: url.index("/posts/")]
            else:
                link_to_profile = post.find_element_by_tag_name("a").get_attribute(
                    "href"
                )
            driver.get(link_to_profile)
            time.sleep(5)
        except:
            logger_screenshot.error(f"Unexpected error: {sys.exc_info()[0]}")
        finally:
            driver.execute_script("document.body.style.zoom = '1.2'")
            capture_profile_page_screenshot(
                background_name=background_name, driver=driver
            )

    # ig capture
    elif link_type == "instagram":
        driver.get(url)
        try:
            time.sleep(5)
            post = driver.find_element_by_tag_name("article")
            is_two_layer = True
            capture_post_screenshot(post, foreground_name, driver)

            # get profile link and capture profile page
            link_to_profile = post.find_element_by_tag_name("a").get_attribute("href")
            driver.get(link_to_profile)
            time.sleep(5)
        except:
            logger_screenshot.error(f"Unexpected error: {sys.exc_info()[0]}")
        finally:
            driver.execute_script("document.body.style.zoom = '1.2'")
            capture_profile_page_screenshot(
                background_name=background_name, driver=driver
            )

    # twi capture
    elif link_type == "twitter":
        # filter url
        if "?" in url:
            url = url[: url.index("?")]

        # get post screenshot
        driver.get(url)

        try:
            time.sleep(5)
            post = driver.find_element_by_tag_name("article")
            is_two_layer = True
            capture_post_screenshot(post, foreground_name, driver)

            # get profile link and capture profile page
            link_to_profile = post.find_element_by_tag_name("a").get_attribute("href")
            driver.get(link_to_profile)
        except:
            logger_screenshot.error(f"Unexpected error: {sys.exc_info()[0]}")
        finally:
            driver.execute_script("document.body.style.zoom = '1.2'")
            time.sleep(5)
            driver.execute_script(
                f"""
            var element = document.querySelector('[class="css-1dbjc4n r-12vffkv"]');
            if (element)
                element.parentNode.removeChild(element);
            """
            )
            capture_profile_page_screenshot(
                background_name=background_name, driver=driver
            )

    elif link_type == "telegram":
        is_two_layer = True
        driver.get(url)
        time.sleep(2)

        driver.execute_script(
            """
        iframe = document.querySelector("iframe");
        iframe.style.padding = "0px";
        element = iframe.contentWindow.document.querySelector(".tgme_widget_message_bubble");
        element.style.border = "0";
        element.style.margin = "0px";

        bubbleTail = iframe.contentWindow.document.querySelector(".tgme_widget_message_bubble_tail");
        if (bubbleTail)
            bubbleTail.parentNode.removeChild(bubbleTail);

        messageWidget = iframe.contentWindow.document.querySelector(".js-widget_message");
        messageWidget.style.padding = "0px";

        """
        )

        driver.execute_script(
            """document.querySelector(".tgme_page_widget_actions").style.visibility = "hidden";"""
        )

        post = driver.find_element_by_tag_name("iframe")
        capture_post_screenshot(post, foreground_name, driver)

        driver.switch_to.frame(post)
        link_to_profile = driver.find_element_by_tag_name("a").get_attribute("href")
        driver.get(link_to_profile)
        time.sleep(1)

        driver.execute_script("window.scrollTo(0, -document.body.scrollHeight)")
        driver.execute_script(
            """loadingElement = document.querySelector(".tme_messages_more js-messages_more");
        if (loadingElement)
            loadingElement.parentNode.removeChild(loadingElement);
        """
        )

        driver.execute_script("document.body.style.zoom = '1.6'")
        capture_profile_page_screenshot(background_name=background_name, driver=driver)

    elif link_type == "scroll":
        driver.get(url)
        # driver.set_window_size(1900,1500)
        driver.execute_script("document.body.style.zoom = '1.0'")
        time.sleep(5)
        capture_profile_page_screenshot(background_name=background_name, driver=driver)

    # quit chrome
    driver.quit()
    
    logger_screenshot.debug(f"Generating and returning SCREENSHOT_DICT")
    # generate screenshot dict for return
    screenshot_dict = {
        "is_two_layer": is_two_layer,
        "bg_path": interlinks.screenshot_folder + "/" + background_name,
        "fg_path": interlinks.screenshot_folder + "/" + foreground_name
        if is_two_layer
        else None,
        "link_type": "instagram" if link_type == "telegram" else link_type,
    }
    return screenshot_dict


def capture_post_screenshot(post, foreground_name, driver):
    logger_screenshot.debug(f"Capturing POST screenshot")
    driver.execute_script("window.scrollTo(0, -document.body.scrollHeight)")
    location = post.location
    size = post.size
    page_rect = driver.execute_cdp_cmd("Page.getLayoutMetrics", {})
    full_post_screenshot = driver.execute_cdp_cmd(
        "Page.captureScreenshot",
        {
            "format": "png",
            "captureBeyondViewport": True,
            "clip": {
                "width": page_rect["contentSize"]["width"],
                "height": page_rect["contentSize"]["height"],
                "x": 0,
                "y": 0,
                "scale": 1,
            },
        },
    )

    logger_screenshot.debug(f"Cropping POST screenshot")
    im = Image.open(BytesIO(base64.urlsafe_b64decode(full_post_screenshot["data"])))
    left = (
        location["x"] * dpi_multiplier
    )  # must mutliply all these numbers by your zoom
    top = location["y"] * dpi_multiplier
    right = (location["x"] + size["width"]) * dpi_multiplier
    bottom = (location["y"] + size["height"]) * dpi_multiplier
    im = im.crop((left, top, right, bottom))  # defines crop points
    im.save(f"{interlinks.screenshot_folder}/{foreground_name}")  # saves new cropped image


def capture_profile_page_screenshot(
    background_name, driver, capture_beyond_viewport=True
):
    logger_screenshot.debug(f"Capturing PROFILE screenshot")
    time.sleep(5)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    driver.execute_script("window.scrollTo(0, -document.body.scrollHeight)")
    time.sleep(3)

    page_rect = driver.execute_cdp_cmd("Page.getLayoutMetrics", {})
    target_height = (
        5000
        if page_rect["contentSize"]["height"] > 5000
        else page_rect["contentSize"]["height"]
    )

    full_page_screenshot = driver.execute_cdp_cmd(
        "Page.captureScreenshot",
        {
            "format": "png",
            "captureBeyondViewport": capture_beyond_viewport,
            "clip": {
                "width": page_rect["contentSize"]["width"]/2,
                "height": target_height,
                "x": 0,
                "y": 0,
                "scale": 1,
            },
        },
    )

    with open(f"{interlinks.screenshot_folder}/{background_name}", "wb") as file:
        file.write(base64.urlsafe_b64decode(full_page_screenshot["data"]))
    return


def process_screenshot_orders():
    logger_screenshot.debug(f"THREAD: Screenshot processor accessed")

    def capturer():
        while db_handler.get_uncaptured_screenshots():
            time.sleep(1)
            order = db_handler.get_uncaptured_screenshots()[0]

            # capture screenshots
            try:
                screenshot_dict = capture_screenshot(url=order["link"])
            except:
                screenshot_dict = False

            if screenshot_dict:
                update_dict = screenshot_dict
                update_dict["screenshots_ready"] = True

                if order["request_type"] == "only_screenshots":
                    update_dict["stage"] = "sending"
                else:
                    update_dict["stage"] = "screenshots_captured"

                db_handler.update_doc_db_parameters(
                    doc_id=order.doc_id, parameters=update_dict
                )

                # start video thread
                if order["request_type"] == "video_auto":
                    render_video_orders()
                else:
                    send_ready_orders()
            else:
                logger_screenshot.error(f"THREAD: Screenshot processor Error")
                bot.send_message(
                    chat_id=order["chat_id"],
                    text="Произошла ошибка захвате скриншотов. Пожалуйста, проверь ссылку и оформи новый заказ через /start. Возможно это ссылка на закрытый профиль.",
                    reply_markup=ReplyKeyboardRemove(),
                )
                db_handler.update_doc_db_parameters(
                    doc_id=order.doc_id,
                    parameters={"status": "error_screenshot_terminated"},
                )

    for thread in threading.enumerate():
        if "capture_screenshots_orders_thread" in thread.name:
            logger_screenshot.debug(f"THREAD: Screenshot processor already runnung")
            return False

    capture_screenshots_orders_thread = threading.Thread(
        target=capturer, args=(), name="capture_screenshots_orders_thread"
    )
    capture_screenshots_orders_thread.start()
    logger_screenshot.debug(f"THREAD: Screenshot processor started")
    return True
