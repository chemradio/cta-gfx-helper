import json
from selenium import webdriver

def remove_ads(driver: webdriver.Chrome) -> None:
    with open('./engines/screenshots/ad_remover_browser_script.js', 'r') as script_file:
        script = script_file.read()

    with open('./engines/screenshots/ad_db.json', 'r') as f:
        ad_db = json.load(f)

    result_script = script + "\n" + "let adsDatabase = " + ad_db + '\n' + "main()"
    driver.execute_script(result_script)
