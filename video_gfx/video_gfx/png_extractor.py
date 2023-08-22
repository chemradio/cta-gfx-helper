import os
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import config

FPS = 25


def extract_png_sequence(html_assembly_name: str) -> str:
    """Extracts PNG-sequence from html gsap animation.
    Returns path to a folder containing the sequence"""

    # helper interpolator
    def interpolation(d, x):
        output = d[0][1] + (x - d[0][0]) * ((d[1][1] - d[0][1]) / (d[1][0] - d[0][0]))
        return output

    # create a driver
    chrome_options = Options()
    chrome_options.add_argument("--allow-file-access-from-files")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.headless = True
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("-–disable-gpu")
    # chrome_options.add_argument("--incognito")
    # chrome_options.add_argument("--disable-web-security") # disabling CORS-conflicts. removes the need to spin-up a web server

    device_emulation = {
        "deviceMetrics": {
            "width": 1920,
            "height": 1080,
            "pixelRatio": 1,
        },
    }
    chrome_options.add_experimental_option("mobileEmulation", device_emulation)

    driver = webdriver.Remote(
        config.REMOTE_VIDEO_GFX_DRIVER_URL, options=chrome_options
    )

    driver.implicitly_wait(5)

    # # previous code
    # html_assembly_server_url = (
    #     f"{config.ASSET_SERVER_ACCESS_URL}/html_assemblies/{html_assembly_name}"
    # )

    html_assembly_server_url = (
        f"{config.ASSET_SERVER_ACCESS_URL}/html_assemblies/{html_assembly_name}"
    )

    target_url = f"{html_assembly_server_url}/main.html"
    print(target_url)
    driver.get(target_url)
    time.sleep(2)

    timeline_duration = driver.execute_script("return timeline.duration()")

    total_frames = timeline_duration * FPS

    interpolation_data = [[0, 0], [total_frames, 1]]

    # create a folder for png-sequence

    png_path = os.path.join(
        f"{config.HTML_ASSEMBLIES_FOLDER}/{html_assembly_name}", "png_sequence"
    )
    os.mkdir(png_path)

    for frame in range(int(total_frames)):
        progress_frame = interpolation(interpolation_data, frame)
        driver.execute_script(f"timeline.progress({progress_frame})")
        driver.save_screenshot(f"{png_path}/{frame:04}.png")
        print(f"Extracting png sequence: {progress_frame*100:.2f}% done", flush=True)

    driver.quit()

    return png_path
