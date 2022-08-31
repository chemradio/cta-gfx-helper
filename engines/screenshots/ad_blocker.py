import json
from selenium import webdriver

def remove_ads() -> None:
    with open('./engines/screenshots/ad_remover_browser_script.js', 'r') as script_file:
        script = script_file.read()

    with open('./engines/screenshots/ad_db.json', 'r') as f:
        ad_db = json.load(f)

    return script + "\n" + "let adsDatabase = " + str(ad_db) + '\n' + "main()"


# print(remove_ads())