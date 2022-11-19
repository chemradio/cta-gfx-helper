from typing import Callable, Dict, List, Optional, Tuple, TypeVar, Union
from telegram import Update
from telegram.utils.helpers import DefaultValue
from telegram.ext import Handler
from telegram.ext.utils.types import CCT


RT = TypeVar('RT')
UT = TypeVar('UT')


class AllHandler(Handler):
    def __init__(self, callback: Callable[[UT, CCT], RT], pass_update_queue: bool = False, pass_job_queue: bool = False, pass_user_data: bool = False, pass_chat_data: bool = False, run_async: Union[bool, DefaultValue] = ...):
        super().__init__(callback, pass_update_queue, pass_job_queue, pass_user_data, pass_chat_data, run_async)


    def check_update(
        self, update: object
    ) -> Optional[Union[bool, Tuple[List[str], Optional[Union[bool, Dict]]]]]:
        if isinstance(update, Update):
            return update
        return None
