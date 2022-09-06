import json
import os
import time
import interlinks
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# VIDEO_LENGTH = 5.0
FPS = 25




def extract_png_sequence(html_assembly_name: str, port:int = 8000) -> str:
    """Extracts PNG-sequence from html gsap animation.
    Returns path to a folder containing the sequence"""

    # helper interpolator
    def interpolation(d, x):
        output = d[0][1] + (x - d[0][0]) * ((d[1][1] - d[0][1])/(d[1][0] - d[0][0]))
        return output

    # create a driver
    chrome_options = Options()
    chrome_options.add_argument('--allow-file-access-from-files')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # chrome_options.headless = True
    # chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--disable-web-security") # disabling CORS-conflicts. removes the need to spin-up a web server
    device_emulation = {"deviceMetrics": {"width": 1920, "height": 1080,"pixelRatio": 1,},}
    chrome_options.add_experimental_option("mobileEmulation", device_emulation)

    if interlinks.USE_REMOTE_DRIVER:
        driver = webdriver.Remote(interlinks.REMOTE_DRIVER_URL, options=chrome_options)
    else:
        driver = webdriver.Chrome(options=chrome_options, service=Service(ChromeDriverManager().install()))

    driver.implicitly_wait(5)

    # # for use with server
    # html_assembly_url = f"http://localhost:{port}/{html_assembly_name}"
    # driver.get(f'{html_assembly_url}/main.html')

    html_assembly_path = f'{interlinks.HTML_ASSEMBLIES_FOLDER}/{html_assembly_name}'
    html_assembly_file_url = f'file://{html_assembly_path}'
    html_assembly_server_url = f'http://localhost:{port}/{html_assembly_name}'
    html_access = html_assembly_file_url

    driver.get(f'{html_access}/main.html')
    time.sleep(2)
    
    # timeline_duration = driver.execute_script('return timeline.duration()')
    with open(f'{html_assembly_path}/config.json') as cfg_file:
        configuration = json.load(cfg_file)
        timeline_duration = configuration['animationDuration'] + interlinks.VIDEO_GFX_TAIL

    total_frames = timeline_duration * FPS

    interpolation_data = [[0, 0],
    [total_frames, 1]]

    # create a folder for png-sequence

    png_path = os.path.join(f'{interlinks.HTML_ASSEMBLIES_FOLDER}/{html_assembly_name}', 'png_sequence')
    os.mkdir(png_path)

    for frame in range(int(total_frames)):
        progress_frame = interpolation(interpolation_data, frame)
        driver.execute_script(f'timeline.progress({progress_frame})')

        # result = driver.execute_script(f'timeline.progress({progress_frame})')
        driver.save_screenshot(f'{png_path}/{frame:04}.png')

    return png_path
