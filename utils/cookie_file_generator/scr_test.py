from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from io import BytesIO
import json
import base64


chrome_options = Options()

chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_experimental_option(
    "mobileEmulation",
    {
        "deviceMetrics": {
            "width": 1920,
            "height": 5760,
            "pixelRatio": 1,
        },
        "userAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    },
)

chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("-–disable-gpu")
# chrome_options.headless = True
chrome_options.add_argument("--headless=new")

driver = webdriver.Remote(
    command_executor="http://127.0.0.1:4444", options=chrome_options
)

t1 = time.perf_counter()
driver.get("https://www.meduza.io/")
t2 = time.perf_counter()

print(f"Time: {t2-t1}")

# driver.save_screenshot("screenshot.png")

chrome_screenshot = driver.command_executor._request(
    "POST",
    driver.command_executor._url
    + f"/session/{driver.session_id}/chromium/send_command_and_get_result",
    json.dumps(
        {
            "cmd": "Page.captureScreenshot",
            "params": {
                "format": "png",
                "captureBeyondViewport": False,
            },
        }
    ),
)

content = BytesIO(base64.urlsafe_b64decode(chrome_screenshot["value"]["data"]))
with open("screenshot.png", "wb") as f:
    f.write(content.getvalue())
driver.quit()
