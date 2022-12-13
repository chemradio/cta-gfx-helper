import json


def remove_ads_script() -> None:
    import requests

    r = requests.get("https://raw.githubusercontent.com/chemradio/cta-chrome-extension/main/ads_database.json")
    js = r.json()


    with open(
        "./screenshots/ad_block/ad_remover_browser_script.js", "r"
    ) as script_file:
        script = script_file.read()

    with open("./screenshots/ad_block/ad_db.json", "r") as f:
        ad_db = json.load(f)

    return script + "\n" + "let adsDatabase = " + str(ad_db) + "\n" + "main()"
