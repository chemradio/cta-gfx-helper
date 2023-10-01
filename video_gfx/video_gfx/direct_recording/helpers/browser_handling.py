import time

from selenium import webdriver


def start_browser(driver: webdriver.Remote, url: str) -> None:
    """
    Open the web-page with animation starting right away.
    The animation is started to pre-cache the moving elements.
    After 2 seconds sleep the animation is paused and reset to the beginning
    thus preparing it to be captured by ffmpeg.
    """
    driver.get(url)
    time.sleep(2)
    driver.execute_script("timeline.pause();")
    driver.execute_script("timeline.progress(0);")


def get_timeline_duration(driver: webdriver.Remote) -> float:
    return driver.execute_script("return timeline.duration()")


def start_animation(driver: webdriver.Remote, delay_secs: int | float = 0) -> None:
    """
    Starts the GSAP animation in the open session of selenium.webdriver.Remote.
    Optionally delays the start by 'sleep' argument.
    """
    if delay_secs > 0:
        time.sleep(delay_secs)

    driver.execute_script("timeline.resume();")
