import json
from pathlib import Path

from selenium import webdriver

JS_TEMPLATE_PATH = Path(__file__).parent / "static" / "adblock_script_template.js"
LOCAL_AD_DB_PATH = Path(__file__).parent / "static" / "ad_db.json"


def generate_adblock_js_script() -> str:
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
        + "try {"
        + "main();"
        + "} catch (e) {"
        + "console.log('Error in main function:', e);"
        + "}"
    )
