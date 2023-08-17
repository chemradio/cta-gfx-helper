import json
from pathlib import Path

import requests
from selenium import webdriver

import config


class Adblocker:
    """Proprietary simple Adblocker. Only one user specific function should be used.
    Provide 'remove_ads' with selenium.webdriver.Chrome instance to execute ad removal.
    """

    @classmethod
    def remove_ads(cls, driver: webdriver.Chrome | webdriver.Remote) -> None:
        ad_db = cls._get_database()
        js_script = cls._generate_js_script(ad_db)
        try:
            driver.execute_script(js_script)
        except:
            print(f"Failed to remove ads from URL: {driver.current_url}")

    @staticmethod
    def _get_database(cls) -> dict:
        r = requests.get(config.REMOTE_ADBLOCK_DB)
        if r.status_code == 200:
            print("Remote adblock database loaded successfully")
            return r.json()

        print(
            f"Local adblock database loaded. Remote failed with status code: {r.status_code}."
        )
        local_ad_db = (
            Path.cwd()
            / "screenshots"
            / "logic"
            / "controllers"
            / "adblocker"
            / "ad_db.json"
        )
        with open(local_ad_db, "r") as f:
            return json.load(f)

    @staticmethod
    def _generate_js_script(ad_db: dict) -> str:
        adblock_script_template_path = (
            Path.cwd()
            / "screenshots"
            / "logic"
            / "controllers"
            / "adblocker"
            / "helpers"
            / "adblock_script_template.js"
        )
        with open(adblock_script_template_path, "r") as script_file:
            script_template = script_file.read()

        return (
            script_template + "\n" + "let adsDatabase = " + str(ad_db) + "\n" + "main()"
        )
