import os
import shutil
import datetime
import json
import interlinks

HTML_TEMPLATE_FOLDER = interlinks.HTML_TEMPLATE_FOLDER
HTML_ASSEMBLIES_FOLDER = interlinks.HTML_ASSEMBLIES_FOLDER

def create_html(parameters: dict = {}) -> str:
    # generate temp folder path
    basename = "gfx_html"
    suffix = datetime.datetime.now().strftime("%Y%m%d_%H-%M-%S_%f")
    target_folder_name = "_".join([basename, suffix])
    target_folder_path = os.path.join(HTML_ASSEMBLIES_FOLDER, target_folder_name)

    # prepack and generate main.html
    # open all referenced js and css and prepack them directly into body of html file
    # prepack_html()
  

    # copy template files
    shutil.copytree(HTML_TEMPLATE_FOLDER, target_folder_path)

    # copy layer images and audio
    assets_to_copy = ('backgroundPath', 'foregroundPath', 'audioPath')

    for asset in assets_to_copy:
        if not parameters.get(asset):
            continue

        asset_path = os.path.abspath(parameters[asset])
        try:
            shutil.copy(asset_path, target_folder_path)
            parameters[asset] = f'./{os.path.basename(asset_path)}'
        except:
            print(__name__, f'Failed to copy {asset}: {asset_path}')
            parameters[asset] = ''
            continue

    # edit template files
    config_json_path = os.path.join(target_folder_path, 'config.json')
    with open(config_json_path, 'w+') as config_file:
        json.dump(parameters, config_file)

    return target_folder_name


def prepack_html():
    # gather js code
    js_files = ('gsap.min.js', 'CustomEase.min.js', 'EasePack.min.js', 'template_builder.js', 'animation.js')

    result_js = '<script>var timeline;</script>'

    for file in js_files:
        with open(f'{HTML_TEMPLATE_FOLDER}/{file}') as f:
            result_js += f'<script>{f.read()}</script>'

    # gather css
    with open(f'{HTML_TEMPLATE_FOLDER}/styles.css') as f:
        result_css = f.read()

    html_result = f'''<!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>{result_css}</style>
    <title>GFX-renderer</title>
    </head>
    <body>
    {result_js}
    </body>
    </html>'''

    with open(f'{HTML_TEMPLATE_FOLDER}/main.html', 'w') as html:
        html.write(html_result)

