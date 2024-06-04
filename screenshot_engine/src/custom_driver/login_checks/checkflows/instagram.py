from selenium import webdriver
from selenium.webdriver.common.by import By


def check_instagram_login(driver: webdriver.Chrome | webdriver.Remote) -> bool:
    # check if not already logged in
    try:
        profile_button = driver.find_element(By.XPATH, "//span[text()='Profile']")
        explore_button = driver.find_element(By.XPATH, "//span[text()='Explore']")
        search_button = driver.find_element(By.XPATH, "//span[text()='Search']")

        # see_all_recomendations_link = driver.find_element(
        #     By.XPATH, "//a[@href='/explore/people' and @role='link']"
        # )
        # search_bar = driver.find_element(
        #     By.XPATH, "//input[@aria-label='Search input' and @type='text']"
        # )
        # profile_button = driver.find_element(By.XPATH, "//span[@role='link']")
        # home_button = driver.find_element(By.XPATH, "//a[@href='/' and @role='link']")
        # likes_button = driver.find_element(By.XPATH, "//a[@href='/accounts/activity']")
        # if it works, we're already logged in
        return True
    except:
        # means we're not logged in
        # continue authentication
        return False
