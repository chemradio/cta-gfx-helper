from multiprocessing import Process
from pathlib import Path

import config

from video_gfx.direct_recording.helpers.browser_handling import (
    get_timeline_duration,
    start_animation,
    start_browser,
)
from video_gfx.direct_recording.helpers.custom_driver import create_driver
from video_gfx.direct_recording.helpers.xvfb_recording import record_selenium_xvfb


def record_gfx(html_assembly_name: str, output_path: str, audio_path: str):
    html_assembly_server_url = (
        f"{config.ASSET_SERVER_ACCESS_URL}/html_assemblies/{html_assembly_name}"
    )

    target_url = f"{html_assembly_server_url}/main.html"
    driver = create_driver()

    start_browser(driver, target_url)

    timeline_duration = get_timeline_duration(driver)

    # signal to start the animation with 0.1 sec delay
    Process(target=start_animation, args=(driver, 0.1)).start()

    # grab the xvfb screen and record
    record_selenium_xvfb(output_path, timeline_duration, audio_path)

    driver.quit()
