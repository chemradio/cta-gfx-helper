import time

from create_driver import create_driver


def perform_test():
    driver = create_driver()

    driver.get("http://server:9000/assets/main.html")
    # driver.get("http://127.0.0.1:9000/assets/main.html")
    time.sleep(3)
    driver.execute_script("timeline.pause()")
    driver.execute_script("timeline.progress(0)")
    driver.execute_script("timeline.resume(0)")
    time.sleep(300)
    driver.quit()

if __name__=="__main__":
    perform_test()