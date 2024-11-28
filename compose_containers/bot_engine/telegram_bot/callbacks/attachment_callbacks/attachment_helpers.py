from typing import List, Set
from telegram import Update, Message


async def attachment_finder(message: Message) -> Set[str]:
    target_keys = ["photo", "document", "audio"]
    return {key for key in target_keys if message.to_dict().get(key)}


async def reply_to_message_parser(update: Update) -> Message:
    try:
        if update.message.reply_to_message:
            return await reply_to_message_parser(update.message.reply_to_message)
        else:
            raise Exception()
    except:
        if isinstance(update, Update):
            return update.message
        elif isinstance(update, Message):
            message = update
            return message
