import os
import psutil
import re
import glob
import interlinks
import shutil
from pathlib import Path
from time import strftime, gmtime
from engines.telegram_bot.bot_instance import bot
from interlinks import cfg

def check_is_url(string):
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex,string)
    return [x[0] for x in url]


def build_assets_folder() -> None:
    folders = (interlinks.USER_FILES_FOLDER,
               interlinks.SCREENSHOT_FOLDER,
               interlinks.RENDER_OUTPUT_PATH,
               interlinks.HTML_ASSEMBLIES_FOLDER)
    for folder in folders:
        try:
            os.mkdir(folder)
        except:
            print(f"Failed to create a folder: {folder}")


def clear_assets_folder(
    user_files:bool = True,
    screenshots: bool = True,
    video_renders: bool = True,
    html_asseblies: bool = True
    ) -> None:
    if user_files:
        shutil.rmtree(interlinks.USER_FILES_FOLDER, ignore_errors=True)
        # files = glob.glob(f'{interlinks.user_files_folder}/*')
        # for file in files:
        #     os.remove(file)
    if screenshots:
        shutil.rmtree(interlinks.SCREENSHOT_FOLDER, ignore_errors=True)
        # files = glob.glob(f'{interlinks.screenshot_folder}/*')
        # for file in files:
        #     os.remove(file)
    if video_renders:
        shutil.rmtree(interlinks.RENDER_OUTPUT_PATH, ignore_errors=True)
        # files = glob.glob(f'{interlinks.render_output_path}/*')
        # for file in files:
        #     os.remove(file)
    if html_asseblies:
        shutil.rmtree(interlinks.HTML_ASSEMBLIES_FOLDER, ignore_errors=True)
        # files = glob.glob(f'{interlinks.HTML_ASSEMBLIES_FOLDER}/*')
        # for file in files:
        #     os.remove(file)

    build_assets_folder()



def calc_readtime(text, wpm=160):
    words = re.findall(r'[а-яА-Яa-zA-Z]+', text)
    digits = re.findall(r'[1-9]', text)
    word_count = len(words) + len(digits)
    seconds = word_count / wpm * 60
    readtime = strftime("%M:%S", gmtime(seconds))
    return readtime


def get_cache_size():
    def folder_size(path=interlinks.ASSETS_FOLDER):
        total = 0
        for entry in os.scandir(path):
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                total += folder_size(entry.path)
        return total

    return int(folder_size() / 1024 / 1024)