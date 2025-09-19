from telegram import Update
from telegram.ext import ContextTypes
from config import TELEGRAM_QUOTE_EDITORS


async def send_quote_for_approval(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    # add quote to db

    # notify editors
    ...
