from dataclasses import dataclass
from telegram_bot.responders.command_responders.exit_responder import ExitResponder
from telegram_bot.responders.command_responders.start_responder import StartResponder
from telegram_bot.responders.command_responders.help_responder import HelpResponder
from telegram_bot.responders.errors_responder import ErrorsResponder
from telegram_bot.responders.request_responders.only_screenshots_responder import (
    OnlyScreenshotsResponder,
)
from telegram_bot.responders.request_responders.readtime_responder import (
    ReadtimeResponder,
)
from telegram_bot.responders.request_responders.video_auto_responder import (
    VideoAutoResponder,
)
from telegram_bot.responders.request_responders.video_files_responder import (
    VideoFilesResponder,
)
from telegram_bot.responders.shared_responders.common_responder import CommonResponder
from telegram_bot.responders.shared_responders.link_responder import LinkResponder
from telegram_bot.responders.shared_responders.quote_responder import QuoteResponder
from telegram_bot.responders.shared_responders.audio_responder import AudioResponder
from telegram_bot.responders.shared_responders.results_responder import ResultsResponder
from telegram_bot.responders.register_responders.register_admin_responder import (
    RegisterAdminResponder,
)
from telegram_bot.responders.register_responders.register_user_responder import (
    RegisterUserResponder,
)


@dataclass
class Responder:
    start = StartResponder
    help = HelpResponder
    exit = ExitResponder

    common = CommonResponder
    errors = ErrorsResponder

    link = LinkResponder
    quote = QuoteResponder
    audio = AudioResponder

    only_screenshots = OnlyScreenshotsResponder
    video_auto = VideoAutoResponder
    video_files = VideoFilesResponder
    readtime = ReadtimeResponder

    results = ResultsResponder

    register_admin = RegisterAdminResponder
    register_user = RegisterUserResponder
