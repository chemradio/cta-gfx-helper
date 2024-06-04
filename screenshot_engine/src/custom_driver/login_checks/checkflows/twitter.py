from selenium import webdriver
from selenium.webdriver.common.by import By


def check_twitter_login(driver: webdriver.Chrome | webdriver.Remote) -> bool:
    try:
        account_menu = driver.find_element(
            By.XPATH, '//div[@aria-label="Account menu"]'
        )
        dmdrawer = driver.find_element(By.XPATH, '//div[@data-testid="DMDrawer"]')
        # if it works, we're already logged in
        return True
    except:
        # means we're not logged in
        # continue authentication
        return False
