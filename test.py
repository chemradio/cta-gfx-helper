from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
from PIL import Image
import time
import base64
from io import BytesIO

dpi_multiplier = 2.0
node_screenshot_offset = [10, 0]
mobile_emulation = { "deviceName": "Selenium-Vertical" }
mobile_emulation = {
    "deviceMetrics": { "width": 1920, "height": 7000, "pixelRatio": 2.0 },
    "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19"
}

chrome_options = Options()

# chrome_options.add_argument(f"--force-device-scale-factor={dpi_multiplier}")
chrome_options.add_argument(f"user-data-dir={os.path.expanduser('~')}/Library/Application Support/Google/Chrome/") #leave out the profile
chrome_options.add_argument("profile-directory=Default") #enter profile here
# chrome_options.add_argument("--window-size=400,1500")
chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)


# mobile_emulation = { "deviceName": "your device" }
# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
# driver = webdriver.Chrome(options=chrome_options) #sometimes you have to insert your execution path
# driver.get('https://www.google.com')

driver = webdriver.Chrome(
    options=chrome_options,
    service=Service(ChromeDriverManager().install())
)

driver.get('https://www.hrw.org/news/2022/07/04/macrons-failed-promises-lebanon')
# driver.set_window_size(400, 1500)

time.sleep(3)

# driver.execute_script("window.scrollTo(0, -document.body.scrollHeight)")

# page_rect = driver.execute_cdp_cmd("Page.getLayoutMetrics", {})
# full_post_screenshot = driver.execute_cdp_cmd(
#     "Page.captureScreenshot",
#     {
#         "format": "png",
#         "captureBeyondViewport": True,
#         "clip": {
#             "width": page_rect["contentSize"]["width"],
#             "height": page_rect["contentSize"]["height"],
#             "x": 0,
#             "y": 0,
#             "scale": 1,
#         },
#     },
# )

# im = Image.open(BytesIO(base64.urlsafe_b64decode(full_post_screenshot["data"])))
# left = (
#     location["x"] * dpi_multiplier
# )  # must mutliply all these numbers by your zoom
# top = location["y"] * dpi_multiplier
# right = (location["x"] + size["width"]) * dpi_multiplier
# bottom = (location["y"] + size["height"]) * dpi_multiplier
# im = im.crop((left, top, right, bottom))  # defines crop points
# im.save(f"{interlinks.screenshot_folder}/{foreground_name}")  # saves new cropped image


# def capture_post_screenshot(post, foreground_name, driver):
#     logger_screenshot.debug(f"Capturing POST screenshot")

# def capture_profile_page_screenshot(
#     background_name, driver, capture_beyond_viewport=True
# ):
#     logger_screenshot.debug(f"Capturing PROFILE screenshot")
#     time.sleep(5)
#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
#     time.sleep(1)
#     driver.execute_script("window.scrollTo(0, -document.body.scrollHeight)")
#     time.sleep(3)

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
        "clip": {
            "width": page_rect["contentSize"]["width"]/2,
            "height": target_height,
            "x": 0,
            "y": 0,
            "scale": 1,
        },
    },
)

with open(f"test.png", "wb") as file:
    file.write(base64.urlsafe_b64decode(full_page_screenshot["data"]))



# def process_screenshot_orders():
#     logger_screenshot.debug(f"THREAD: Screenshot processor accessed")

#     def capturer():
#         while db_handler.get_uncaptured_screenshots():
#             time.sleep(1)
#             order = db_handler.get_uncaptured_screenshots()[0]

#             # capture screenshots
#             try:
#                 screenshot_dict = capture_screenshot(url=order["link"])
#             except:
#                 screenshot_dict = False

#             if screenshot_dict:
#                 update_dict = screenshot_dict
#                 update_dict["screenshots_ready"] = True

#                 if order["request_type"] == "only_screenshots":
#                     update_dict["stage"] = "sending"
#                 else:
#                     update_dict["stage"] = "screenshots_captured"

#                 db_handler.update_doc_db_parameters(
#                     doc_id=order.doc_id, parameters=update_dict
#                 )

#                 # start video thread
#                 if order["request_type"] == "video_auto":
#                     render_video_orders()
#                 else:
#                     send_ready_orders()
#             else:
#                 logger_screenshot.error(f"THREAD: Screenshot processor Error")
#                 bot.send_message(
#                     chat_id=order["chat_id"],
#                     text="Произошла ошибка захвате скриншотов. Пожалуйста, проверь ссылку и оформи новый заказ через /start. Возможно это ссылка на закрытый профиль.",
#                     reply_markup=ReplyKeyboardRemove(),
#                 )
#                 db_handler.update_doc_db_parameters(
#                     doc_id=order.doc_id,
#                     parameters={"status": "error_screenshot_terminated"},
#                 )

#     for thread in threading.enumerate():
#         if "capture_screenshots_orders_thread" in thread.name:
#             logger_screenshot.debug(f"THREAD: Screenshot processor already runnung")
#             return False

#     capture_screenshots_orders_thread = threading.Thread(
#         target=capturer, args=(), name="capture_screenshots_orders_thread"
#     )
#     capture_screenshots_orders_thread.start()
#     logger_screenshot.debug(f"THREAD: Screenshot processor started")
#     return True
