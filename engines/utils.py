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
from os_scripts.os_script_handler import os_script

def check_is_url(string):
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex,string)
    return [x[0] for x in url]


def build_assets_folder() -> None:
    folders = (interlinks.user_files_folder,
               interlinks.screenshot_folder,
               interlinks.render_output_path,
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
        shutil.rmtree(interlinks.user_files_folder)
        # files = glob.glob(f'{interlinks.user_files_folder}/*')
        # for file in files:
        #     os.remove(file)
    if screenshots:
        shutil.rmtree(interlinks.screenshot_folder)
        # files = glob.glob(f'{interlinks.screenshot_folder}/*')
        # for file in files:
        #     os.remove(file)
    if video_renders:
        shutil.rmtree(interlinks.render_output_path)
        # files = glob.glob(f'{interlinks.render_output_path}/*')
        # for file in files:
        #     os.remove(file)
    if html_asseblies:
        shutil.rmtree(interlinks.HTML_ASSEMBLIES_FOLDER)
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


def get_adobe_running():
    class RunningProcesses:
        def __init__(self):
            self.ae_running = False
            self.ame_running = False

    running_processes = RunningProcesses()

    process_list = []
    for process in psutil.process_iter():
        process_list.append(process.name())
    
    running_processes.ae_running = True if 'After Effects' in process_list else False
    running_processes.ame_running = True if f'Adobe Media Encoder {cfg["adobe_version"]}' in process_list else False

    return running_processes


def restart_adobe_apps_util(admin_id):
    running_apps = get_adobe_running()

    if running_apps.ae_running:
        bot.send_message(chat_id=admin_id, text='Shutting down AfterFX')
        os_script.quit_ae()

    if running_apps.ame_running:
        bot.send_message(chat_id=admin_id, text='Shutting down Encoder')
        os_script.quit_ame()

    bot.send_message(chat_id=admin_id, text='Relaunching AfterFX')
    os_script.start_ae()

    bot.send_message(chat_id=admin_id, text='Relaunching Encoder')
    os_script.start_ame()

    running_apps = get_adobe_running()
    if running_apps.ae_running and running_apps.ame_running:
        bot.send_message(chat_id=admin_id, text='Adobe Apps successfully relaunched')
        return True
    else:
        bot.send_message(chat_id=admin_id, text='Something in wrong')
        return False


def get_chrome_running():
    process_list = []
    for process in psutil.process_iter():
        process_list.append(process.name())
        return True if "Google Chrome" in process_list else False


def quit_chrome(admin_id):
    if get_chrome_running():
        for i in range(5):
            try:
                os_script.quit_chrome()
            except:
                pass
    bot.send_message(chat_id=admin_id, text='Chrome Quitted')


def get_cache_size():
    def folder_size(path=interlinks.assets_folder):
        total = 0
        for entry in os.scandir(path):
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                total += folder_size(entry.path)
        return total

    return int(folder_size() / 1024 / 1024)