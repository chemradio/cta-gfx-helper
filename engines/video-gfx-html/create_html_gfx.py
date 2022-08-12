import os
import shutil
import datetime
import json

HTML_TEMPLATE_FOLDER = os.path.abspath('./html/html_template')

def create_html(parameters: dict = {}) -> str:
    # generate temp folder path
    basename = "gfx_html"
    suffix = datetime.datetime.now().strftime("%Y%m%d_%H-%M-%S_%f")
    target_folder_name = "_".join([basename, suffix])
    target_folder_path = os.path.abspath(f'./html/html_assemblies/{target_folder_name}')

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
    with open(f'{target_folder_path}/config.json', 'w+') as config_file:
        json.dump(parameters, config_file)

    return target_folder_name


if __name__ == '__main__':
    params = {
        'bg_class': 'bgOnly',
        'bg_path': os.path.abspath('./01_BG_2fd26050c5df9b57.png'),
        'fg_class': 'twitter',
        'fg_path': os.path.abspath('./02_FG_56de5e33650775e4.png'),
        'round_corners': 'round-corners',
        'quote_text_text': 'Some quote text here...',
        'quote_author_text': 'Quote Author',
        'single_layer_trigger': ''
    }

    create_html(params)