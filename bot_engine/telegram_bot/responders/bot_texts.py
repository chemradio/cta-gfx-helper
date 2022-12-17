from dataclasses import dataclass


@dataclass
class ErrorResponses:
    gp_error: str = "🆘 Что-то пошло не так. Попробуй снова или начни сначала - /exit"
    try_again_error: str = "🆘 Что-то пошло не так. Попробуй снова."
    no_active_session_notification: str = "💡 Сначала нажми /start"
    wrong_audio_format: str = "🆘🔊 Этот аудио-файл не поддерживается. Или это вовсе не аудио. Попробуй другой файл."
    audio_duration_exceeded: str = (
        "🆘🔊 Этот аудио-файл длиннее 40 секунд. Попробуй другой."
    )


@dataclass
class QuoteResponses:
    quote_enabled: str = "📜 Нужна 'коробка-цитата' на графику?"
    quote_text: str = "📜 Введи текст цитаты. Без кавычек, без автора."
    quote_author_enabled: str = "📜 Нужно указать автора цитаты?"
    quote_author_text: str = "📜 Введи имя автора и его должность через запятую."


@dataclass
class AudioResponses:
    audio_enabled: str = "🔊 Подложить звук?"
    send_audio: str = (
        "🔊 Пришли мне аудио-файл в формате MP3 или WAV. Не длиннее 30 секунд."
    )


@dataclass
class VideoFilesResponses:
    bg_animation_type: str = "🎨 Выбери тип анимации для заднего фона."
    bg_animation_type_responded: str = "🎨 Анимация заднего фона: {bg_animation}"
    seng_bg: str = "🎨 Пришли изображение для заднего плана."
    fg_enabled: str = "🎨 Будет передний план?"
    seng_fg: str = "🎨 Пришли мне изображение для переднего плана."
    fg_animation_type: str = "🎨 Выбери тип анимации для переднего плана."
    fg_animation_type_responded: str = "🎨 Анимация переднего плана: {fg_animation}"
    round_corners_enabled: str = "🎨 Закруглить края переднего фона?"


@dataclass
class ReadtimeResponses:
    send_text: str = "📝 Пришли сюда текст."
    bad_text: str = "📝 Это не текст. Скопируй текст в сообщение."
    set_speed: str = "📝 Выбери скорость чтения."
    set_speed_responded: str = "📝 Скорость чтения: {speed}."
    results: str = "📝 На скорости {speed} слов в минуту хрон текста - {readtime}"


@dataclass
class CommonResponses:

    sessions_terminated_start: str = (
        "❎ Все предыдущие заказы отменены. Новый заказ - /start"
    )
    terminate_sessions_notification: str = (
        "❌ Пожалуйста, отмени предыдущий незавершенный заказ командой /exit"
    )
    start_new_session: str = "💡 Новый заказ - /start"
    wait_for_gfx: str = "⏳ Пожалуйста, подожди. Скоро твоя видео-графика будет готова."
    wait_for_processing: str = "⏳ Заказ все еще обрабатывается. Пожалуйста, подожди."


@dataclass
class LinkResponses:
    link: str = "🔗 Пришли нужную ссылку."
    bad_link: str = "🆘🔗 Не могу обработать эту ссылку. Пожалуйста, пришли другую."


@dataclass
class RegisterResponses:
    register_not_applied: str = "👤 💡 Зарегистрируйся - /register"
    register_already_applied: str = "👤 💡 Твой запрос еще на рассмотрении. Ожидай."
    register_already_approved: str = "👤 💡 Ты уже зарегистрирован."

    register_applied_user: str = (
        "👤 💡 Твоя заявка на регистрацию принята. Пожалуйста, ожидай."
    )
    register_approved_user: str = (
        "👤 ✅ Твоя заявка на регистрацию одобрена. Начни новый заказ - /start"
    )
    register_pending_user: str = (
        "👤 ⌛ Твоя заявка на регистрацию все еще на рассмотрении."
    )

    register_applied_admin: str = "👤 💡 Новая заявка на регистрацию.\n\nИмя: {first_name}\nTelegram ID: {telegram_id}"
    register_approved_admin: str = "👤 ✅ Заявка на регистрацию одобрена.\n\nИмя: {first_name}\nTelegram ID: {telegram_id}"
    register_blocked_admin: str = "👤 ❌ Пользователь заблокирован.\n\nИмя: {first_name}\nTelegram ID: {telegram_id}"
    register_pended_admin: str = (
        "👤 ❔ Пользователь в ожидании.\n\nИмя: {first_name}\nTelegram ID: {telegram_id}"
    )
    empty_users_list: str = "👤... Пользователи с таким критерием отсутствуют"

    list_pending_user: str = "👤 ❔ Неодобренный пользователь.\n\nИмя: {first_name}\nTelegram ID: {telegram_id}"
    list_approved_user: str = (
        "👤 ✅ Одобренный пользователь.\n\nИмя: {first_name}\nTelegram ID: {telegram_id}"
    )
    list_blocked_user: str = "👤 ❌ Заблокированный пользователь.\n\nИмя: {first_name}\nTelegram ID: {telegram_id}"

    pend_inline: str = "❔ Решить позже"
    approve_inline: str = "✅ Одобрить"
    block_inline: str = "❌ Заблокировать"


@dataclass
class CommandResponses:
    start_message: str = "🍱 Выбери тип заказа:"
    start_message_edited: str = "🍱 Тип заказа:"
    help_message: str = "💡 ..."
    exit_message: str = "❎ Текущий заказ отменен. Начать новый - /start"
    exit_message_missing_orders: str = (
        "❎ У тебя нет незавершенных заказов. Начать новый - /start"
    )


@dataclass
class RequestOptions:
    video_auto: str = "Графика из ссылки"
    video_files: str = "Графика из файлов"
    only_screenshots: str = "Только скриншоты"
    readtime: str = "Хрон текста"


@dataclass
class ResultsResponses:
    request_type: str = "🍱 Тип заказа:"

    link: str = "🔗 Ссылка для графики:"

    bg_animation: str = "🎨 Анимация заднего плана:"
    fg_enabled: str = "🎨 Передний план:"
    fg_animation: str = "🎨 Анимация переднего плана:"

    quote_enabled: str = "📜 Цитата:"
    quote_text: str = "📜 Текст цитаты:"
    quote_author_enabled: str = "📜 Указать автора цитаты:"
    quote_author_text: str = "📜 Автор цитаты:"

    audio_enabled: str = "🔊 Аудио-файл:"

    readtime_text: str = "📝 Текст:"
    readtime_speed: str = "📝 Скорость чтения:"
    readtime_result: str = "📝 Хрон текста на этой скорости:"

    results_correct = "✅ Заказ принят, ожидай. Или начни следющий - /start"
    results_incorrect = "❌ Заказ отменен. Начать новый - /start"


@dataclass
class AdminResponses:
    admin_panel: str = "⌘ Панель администратора"

    list_10_orders: str = "🧾 Последние 10 заказов"
    list_active_orders: str = "⏳ Активные заказы"

    list_approved_users: str = "👍 Одобренные пользователи"
    list_blocked_users: str = "🛑 Заблокированные пользователи"
    list_pending_users: str = "❔ Ожидающие пользователи"

    cancel_order: str = "🛑 Отменить заказ"

    list_single_order: str = """Заказ № {order_id}

Заказчик: {customer_name}
Тип заказа: {request_type}
Cтатус: {status}
Время ожидания: {wait_time}

Ссылка: {link}
Цитата: {quote_text}
Автор цитаты: {quote_author}
Звук: {audio_enabled}"""

    cookie_file_successfully_uploaded: str = "Cookie-файл загружен успешно"
    cookie_file_upload_failed: str = "Ошибка загрузки cookie-файла"


@dataclass
class Responses:
    admin = AdminResponses
    error = ErrorResponses
    quote = QuoteResponses
    audio = AudioResponses
    video_files = VideoFilesResponses
    readtime = ReadtimeResponses
    common = CommonResponses
    link = LinkResponses
    register = RegisterResponses
    command = CommandResponses
    results = ResultsResponses
    request_options = RequestOptions
    register = RegisterResponses
