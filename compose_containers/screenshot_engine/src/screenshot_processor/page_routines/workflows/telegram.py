from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


def telegram_post_routine(driver: webdriver.Remote) -> WebElement:
    driver.execute_script(
        """iframe = document.querySelector("iframe");
        iframe.style.padding = "0px";
        element = iframe.contentWindow.document.querySelector(".tgme_widget_message_bubble");
        element.style.border = "0";
        element.style.margin = "0px";

        bubbleTail = iframe.contentWindow.document.querySelector(".tgme_widget_message_bubble_tail");
        if (bubbleTail)
            bubbleTail.parentNode.removeChild(bubbleTail);

        messageWidget = iframe.contentWindow.document.querySelector(".js-widget_message");
        messageWidget.style.padding = "0px";"""
    )
    # driver.execute_script(
    #     """document.querySelector(".tgme_page_widget_actions").style.visibility = "hidden";"""
    # )
    post = driver.find_element(By.TAG_NAME, "iframe")
    return post


def telegram_profile_routine(driver: webdriver.Remote) -> WebElement:
    driver.execute_script("window.scrollTo(0, -document.body.scrollHeight)")
    driver.execute_script(
        """loadingElement = document.querySelector(".tme_messages_more js-messages_more");
    if (loadingElement)
        loadingElement.parentNode.removeChild(loadingElement);
    """
    )
    driver.execute_script("document.body.style.zoom = '1.6'")
    return driver.find_element(By.TAG_NAME, "body")


def extract_telegram_profile_url(driver: webdriver.Remote) -> str:
    try:
        effective_path = driver.current_url.split("//t.me/")[1]
        return f"https://t.me/s/{effective_path}"
    except:
        return f"https://t.me/"
