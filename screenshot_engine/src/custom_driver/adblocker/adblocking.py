import json
from pathlib import Path

from selenium import webdriver

JS_TEMPLATE_PATH = Path(__file__).parent / "adblock_script_template.js"
LOCAL_AD_DB_PATH = Path(__file__).parent / "ad_db.json"


def remove_ads(driver: webdriver.Chrome | webdriver.Remote) -> None:
    js_script = _generate_js_script()
    try:
        print("trying to remove ads", flush=True)
        driver.execute_script(js_script)
        print("Success in removing ads", flush=True)
    except Exception as e:
        print(f"Failed to remove ads from URL: {driver.current_url}", flush=True)
        print(str(e), flush=True)


def _generate_js_script() -> str:
    with open(LOCAL_AD_DB_PATH, "r") as f:
        ad_db = json.load(f)
    with open(JS_TEMPLATE_PATH, "r") as script_file:
        script_template = script_file.read()

    return (
        script_template
        + "\n"
        + "let adsDatabase = "
        + str(ad_db)
        + "\n"
        + "removeAdsMedium();"
        + "\n"
        + "main();"
    )
