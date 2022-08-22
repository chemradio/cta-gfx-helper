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
    # chrome_options.add_argument('--allow-file-access-from-files')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.headless = True
    device_emulation = {"deviceMetrics": {"width": 1920, "height": 1080,"pixelRatio": 1,},}
    chrome_options.add_experimental_option("mobileEmulation", device_emulation)
    driver = webdriver.Chrome(options=chrome_options, service=Service(ChromeDriverManager().install()))
    driver.implicitly_wait(5)

    html_assembly_url = f"http://localhost:{port}/{html_assembly_name}"
    driver.get(f'{html_assembly_url}/main.html')
    time.sleep(2)
    
    timeline_duration = driver.execute_script('return timeline.duration()')
    total_frames = timeline_duration * FPS

    interpolation_data = [[0, 0],
    [total_frames, 1]]

    # create a folder for png-sequence

    png_path = os.path.join(f'{interlinks.HTML_ASSEMBLIES_FOLDER}/{html_assembly_name}', 'png_sequence')
    os.mkdir(png_path)

    for frame in range(int(total_frames)):
        progress_frame = interpolation(interpolation_data, frame)
        result = driver.execute_script(f'timeline.progress({progress_frame})')
        driver.save_screenshot(f'{png_path}/{frame:04}.png')

    return png_path


# testing
if __name__ == "__main__":
    extract_png_sequence('/Users/tim/code/ae-to-html/html/html_assemblies/gfx_html_20220811_02-21-37_365727')
