from telegram import Update
from telegram.ext import BaseHandler


class AllHandler(BaseHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def check_update(self, update):
        if isinstance(update, Update):
            return update
        return None
