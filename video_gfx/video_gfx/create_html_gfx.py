import datetime
import json
import os
import shutil

import config

HTML_TEMPLATE_FOLDER = config.HTML_TEMPLATE_FOLDER
HTML_ASSEMBLIES_FOLDER = config.HTML_ASSEMBLIES_FOLDER


def create_html(parameters: dict, html_assembly_path: str) -> str:
    try:
        # copy template files
        shutil.copytree(HTML_TEMPLATE_FOLDER, html_assembly_path)

        # copy layer images and audio
        assets_to_copy = ("backgroundPath", "foregroundPath", "audioPath")

        for asset in assets_to_copy:
            if not parameters.get(asset):
                continue

            asset_path: str = os.path.abspath(parameters[asset])
            try:
                shutil.copy(asset_path, html_assembly_path)
                parameters[asset] = f"./{os.path.basename(asset_path)}"
            except:
                print(__name__, f"Failed to copy {asset}: {asset_path}")
                parameters[asset] = ""
                continue

        # edit template files
        config_json_path = os.path.join(html_assembly_path, "config.json")
        with open(config_json_path, "w+") as config_file:
            json.dump(parameters, config_file)

        return True
    except:
        return False
