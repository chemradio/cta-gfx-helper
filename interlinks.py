import os
import json
with open('config_and_db/config.json') as cf:
    cfg = json.loads(cf.read())


# telegram bot
BOT_TOKEN = cfg['bot_token']


# configure paths
BASE_PATH = os.getcwd()
ASSETS_FOLDER = os.path.join(BASE_PATH, "assets/")
SCREENSHOT_FOLDER = os.path.join(ASSETS_FOLDER + "screenshots/")
USER_FILES_FOLDER = os.path.join(ASSETS_FOLDER + "user_files/")
RENDER_OUTPUT_PATH = os.path.join(ASSETS_FOLDER + "video_exports")
RECENT_ORDERS_INTERVAL_HOURS = 300

# misc
RESCAN_INTERVAL = 20
EXPIRY_INTERVALS_SECS = 300
ADMIN_TELEGRAM_IDS = cfg['admin_telegram_ids']
EDITOR_IDS = cfg['editor_ids']
DELEGATE_EDITOR = EDITOR_IDS["editor_name"]

# screenshots
DPI_MULTIPLIER = 2.0
SCREENSHOT_ATTEMPTS = 2
COOKIE_FILE = 'config_and_db/cookie_file.json'
SOCIAL_WEBSITES = {'facebook': 'https://facebook.com', 'twitter': 'https://twitter.com', 'instagram': 'https://instagram.com', 'telegram': 'https://telegram.org'}
LOGIN_REQUIRED = (
    'instagram',
    'facebook',
    # 'twitter',
)

LOGIN_TO_SOCIAL_WEBSITES = True
logged_in_to_social_websites = True


# docker
USE_DOCKER = False

# assets server
ASSET_SEVER_NAME = 'html_server'
ASSET_SERVER_PUBLISH_URL = '0.0.0.0'
ASSET_SERVER_ACCESS_URL = ASSET_SEVER_NAME if USE_DOCKER else 'localhost'
ASSET_SERVER_ACCESS_PORT = 9000

# selenium remote webdriver
USE_REMOTE_DRIVER = USE_DOCKER
REMOTE_DRIVER_HOST = 'chrome'
REMOTE_DRIVER_PORT = 4444
REMOTE_DRIVER_URL = f"http://{REMOTE_DRIVER_HOST}:{REMOTE_DRIVER_PORT}/wd/hub"
SELENIUM_DOCKER_CMD = 'docker run -d --rm -it -p 4444:4444 -p 5900:5900 -p 7900:7900 --shm-size 3g --net="host" seleniarm/standalone-chromium:latest'


# video-gfx
MAX_AUDIO_FILE_LENGTH = 30
AUDIO_OFFSET = .3
VIDEO_GFX_TAIL = 2.0

HTML_ASSETS_FOLDER = os.path.join(BASE_PATH, 'engines/video_gfx_html/html')
HTML_TEMPLATE_FOLDER = os.path.join(HTML_ASSETS_FOLDER, 'html_template')
HTML_ASSEMBLIES_FOLDER = os.path.join(ASSETS_FOLDER, 'html_assemblies')




















help_text = """Ты можешь:

Заказать скриншоты с веб-страницы. Если это соцсеть - ты получишь сразу 2 скриншота - поста и профиля.
Ты также можешь заказать анимированную видео-графику из этих скриншотов. Если хочешь - бот еще и цитату добавит.

Когда будешь отправлять ссылку на веб страницу, убедись, что в твоем сообщении нет ничего кроме этой ссылки.

Если это ссылка из соцсети (Facebook, Instagram или Twitter) - убедись, что отправляешь ссылку на ПУБЛИКАЦИЮ, а не на профиль.

Бот работает в тестовом режиме.

Если возникнут проблемы с ботом - сделай скриншот переписки с ботом с самого начала заказа и отправь его автору в телегу - @chemradio.

Удачи!

/start - начало работы с ботом.

/video_auto - чтобы бот сделал видео-графику из скриншотов страницы, на которую у тебя есть ссылка.

/video_files - чтобы бот сделал видео-графику из файлов, которые у тебя уже есть. Например, скриншот сайта и PDF-файл оттуда

/only_screenshots - чтобы бот отправил тебе только скриншоты страницы, на которую у тебя есть ссылка.

/exit - завершить текущую сессию, чтобы начать заново.

/help - описание бота.

"""

admin_commands = """

/send_announcement

/register_requests
/registered_users
/blocked_users

/active_orders
/processing_orders
/recent_orders
/terminate_sessions

/check_adobe_running
/restart_adobe_apps
/start_adobe_apps
/quit_adobe_apps

/check_chrome_running
/quit_chrome

/cache_size
/clear_bot_cache
"""

# texts
stage_texts = {
    "common": {
        "link": "<b><u>ССЫЛКА</u></b>\n\nПришли мне сюда нужную <b>ссылку</b>.",
        "yes_answer": "Да",
        "no_answer": "Нет",
        "start_message": "Привет! Нажми на команду:\n\n<b>/video_auto</b> - <i>видео-графика из ссылки</i>\n<b>/video_files</b> - <i>видео-графика из файлов</i>\n<b>/only_screenshots</b> - <i>скриншоты из ссылки</i>\n\n<b>/readtime</b> - <i>хрон текста</i>\n\n<b>/exit</b> - <i>завершить текущую сессию</i>\n<b>/back</b> - <i>шаг назад, глючит</i>\n\n<b>/help</b> - <i>описание бота</i>",
        "sessions_terminated_start": "<i>Все предыдущие сессии завершены.</i>\n\nНажми <b>/start</b> для начала работы с ботом.\n<b>/help</b> - описание бота.",
        "terminate_sessions_notification": "Пожалуйста, заверши предыдущие сессии командой /exit.",
        "start_new_session": "<b>/start</b> - начать новую сессию",
        "wait_for_gfx": "Пожалуйста, подожди. Скоро твоя видео-графика будет готова.",
        "wait_for_processing": "Заказ все еще обрабатывается. Пожалуйста, подожди.",
    },
    "quote": {
        "quote_enabled": "<b><u>ЦИТАТА</u></b>\n\n<b>Нужна 'коробка-цитата' на видео?</b>",
        "quote_text": "<b><u>ЦИТАТА</u></b>\n\n<b>Введи сюда текст цитаты.</b>\n\n<i>Не ставь кавычки. Не указывай автора, укажем позже, если надо.\nВычитай текст перед отправкой.</i>",
        "quote_author_enabled": "<b><u>ЦИТАТА</u></b>\n\n<b>Нужно указать автора цитаты?</b>",
        "quote_author_text": "<b><u>ЦИТАТА</u></b>\n\n<b>Введи сюда имя автора и его должность через запятую.</b>\n\n<i>Внимательно вычитай перед отправкой.\n<b>ПРИМЕР:\n</b> Антонио Вивальди, композитор</i>",
    },
    "audio": {
        "audio_enabled": "<b><u>АУДИО</u></b>\n\n<b>У тебя есть готовый аудио-файл для подложки на графику?</b>",
        "send_audio": f"<b><u>АУДИО</u></b>\n\n<b>Пришли мне этот аудио-файл в формате MP3 или WAV.</b>\n\n<i>Аудио должно быть не длиннее {str(MAX_AUDIO_FILE_LENGTH)} секунд</i>",
    },
    # 'video_auto':
    # 'link':
    # 'quote_enabled':
    # 'quote_text':
    # 'quote_author_enabled':
    # 'quote_author_text':
    # 'audio_enabled':
    # 'send_audio':
    # 'check':
    "video_files": {
        "bg_animation_type": "<b><u>ЗАДНИЙ ПЛАН</u></b>\n\n<b>Выбери тип анимации для заднего фона.</b>\n\n<i>Если это скриншот веб-страницы, выбери Scroll.\nЕсли это фото-подложка, выбери Zoom.</i>",
        "seng_bg": "<b><u>ЗАДНИЙ ПЛАН</u></b>\n\n<b>Пришли мне изображение для заднего плана.</b>\n\n<i>Это может быть PNG, JPG или PDF файл.</i>",
        "fg_enabled": "<b><u>ПЕРЕДНИЙ ПЛАН</u></b>\n\n<b>Будет передний план?</b>",
        "seng_fg": "<b><u>ПЕРЕДНИЙ ПЛАН</u></b>\n\n<b>Пришли мне изображение для переднего плана.</b>\n\n<i>Это может быть PNG, JPG или PDF файл.</i>",
        "fg_animation_type": "<b><u>ПЕРЕДНИЙ ПЛАН</u></b>\n\n<b>Выбери тип анимации для переднего плана.</b>\n\n<i>Если это просто картинка - выбери Instagram.\nЕсли это PFD файл - выбери Document.</i>",
        "round_corners_enabled": "<b>Закруглить края переднего фона?</b>",
    },
    "readtime": {
        "send_text": "<b><u>ХРОН ТЕКСТА</u></b>\n\n<b>Пришли сюда текст.</b>\n\n<i>Отправь только текст. Остальное я не пойму.</i>",
        "set_speed": "<b><u>ХРОН ТЕКСТА</u></b>\n\n<b>Выбери скорость чтения.</b>",
    },
    #
    # 'send_fg':
    # 'quote_enabled':
    # 'quote_text':
    # 'quote_author_enabled':
    # 'quote_author_text':
    # 'audio_enabled':
    # 'send_audio':
    # 'check':
    # 'only_screenshots':
    # 'link':
    "error": "Что-то пошло не так. Нажми <b>/exit</b>, а потом <b>/start</b>.",
    "wrong_link": "Не могу обработать эту ссылку. Пожалуйста, пришли другую.",
    "wait_for_render": "Пожалуйста, подожди. Скоро твоя видео-графика будет готова.",
    "wait_for_order": "Заказ все еще обрабатывается. Пожалуйста, подожди.",
    "make_new_order": "Оформи новый заказ через <b>/start</b>.",
    "weird_error": "Вообще не понятно, что произошло. Тыкни <b>/start</b>",
    "try_again": "Что-то пошло не так. Попробуй заново.",
    "no_active_session": "Нет активной сессии. Нажми <b>/start</b> для начала работы.",
    "unnecessary_file": "Сейчас мне не нужен файл. Начни новую сессию через команду <b>/start</b>.",
    "unregistered_user": "Тебя нет в списке зарегистрированных пользователей. Подай заявку через <b>/register</b>.",
    "register_applied": "Твой запрос отправлен. Ожидай.",
    "already_in_db": "Твой запрос уже на рассмотрении.",
}


quote_checker = {
    "main": "Это основное уведомление. А тут текст цитаты {}",
    "text": "Это уведомление, содержащее текст цитаты",
    "author": "Это уведомление с автором цитаты",
    "final": "Это уведомление для финального подтверждения",
}
