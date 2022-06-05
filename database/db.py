import sys
sys.path.append('..')

from tinydb import TinyDB, Query
from tinydb.table import Document
from threading import RLock
from engines.telegram_bot import bot
import time
import interlinks
import logging
import datetime

logger_db = logging.getLogger(__name__)
logger_db.setLevel(logging.DEBUG)

logging_db_formatter = logging.Formatter("%(asctime)s: %(name)s: %(message)s")

# logging_db_file_handler = logging.FileHandler(f'./logs/{__name__}.log')
# logging_db_file_handler.setLevel(logging.DEBUG)
# logging_db_file_handler.setFormatter(logging_db_formatter)

logging_db_stream_handler = logging.StreamHandler()
logging_db_stream_handler.setFormatter(logging_db_formatter)

# logger_db.addHandler(logging_db_file_handler)
# logger_db.addHandler(logging_db_stream_handler)


main_db_lock = RLock()


def thread_safe(func):
    def wrapper_thread_safe(*args, **kwargs):
        with main_db_lock:
            # logger_db.debug(f"Calling {func.__name__}")
            value = func(*args, **kwargs)
            # logger_db.debug(f"{func.__name__!r} returned {value!r}")
            return value

    return wrapper_thread_safe


class TinyDBHandler:
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(TinyDBHandler, cls).__new__(cls)
        return cls.instance

    def __init__(self) -> None:
        self.db_orders = TinyDB("config_and_db/db_orders.json")
        self.db_allowed_users = TinyDB("config_and_db/db_allowed_users.json")
        self.db_sys_events = TinyDB("config_and_db/system_events.json")
        self.db_sys_events.truncate()

    @thread_safe
    def add_db_entry(self, parameters):
        return self.db_orders.insert(parameters)

    @thread_safe
    def get_init_status(self, user_id):
        db_query = Query()
        results = self.db_orders.search(
            (db_query.status == "init") & (db_query.telegram_id == user_id)
        )
        if results:
            # terminate previous active sessions
            if len(results) > 1:
                for i in range(len(results) - 1):
                    self.db_orders.update(
                        {"status": "error_terminated"}, doc_ids=[results[i].doc_id]
                    )
            return results[-1].doc_id
        else:
            return False

    @thread_safe
    def activate_init_status(self, user_id):
        doc_id = self.get_init_status(user_id=user_id)
        if doc_id:
            self.db_orders.update({"status": "active"}, doc_ids=[doc_id])

    @thread_safe
    def get_active_doc_id(self, user_id):
        db_query = Query()
        results = self.db_orders.search(
            (db_query.status == "active") & (db_query.telegram_id == user_id)
        )
        if results:
            # terminate previous active sessions
            if len(results) > 1:
                for i in range(len(results) - 1):
                    self.db_orders.update(
                        {"status": "error_terminated"}, doc_ids=[results[i].doc_id]
                    )
            return results[-1].doc_id
        else:
            return False

    @thread_safe
    def get_current_stage(self, user_id):
        doc_id = self.get_active_doc_id(user_id)
        if doc_id:
            query = self.db_orders.get(doc_id=doc_id)
            return query["stage"]
        else:
            return False

    @thread_safe
    def set_user_stage(self, user_id, stage):
        doc_id = self.get_active_doc_id(user_id)
        if doc_id:
            self.db_orders.update({"stage": stage}, doc_ids=[doc_id])
            return True
        else:
            return False

    @thread_safe
    def update_db_parameters(self, user_id, parameters):
        doc_id = self.get_active_doc_id(user_id)
        if doc_id:
            for key in parameters:
                self.db_orders.update({key: parameters[key]}, doc_ids=[doc_id])
            return True
        else:
            return False

    @thread_safe
    def update_doc_db_parameters(self, doc_id, parameters):
        if doc_id:
            for key in parameters:
                self.db_orders.update({key: parameters[key]}, doc_ids=[doc_id])
            return True
        else:
            return False

    @thread_safe
    def get_active_entry_data(self, user_id):
        query = self.db_orders.get(doc_id=self.get_active_doc_id(user_id))
        if query:
            return query
        else:
            return False

    @thread_safe
    def get_unchecked_quotes(self):
        db_query = Query()
        result = self.db_orders.search(db_query.stage == "check_quote")
        if result:
            return result
        else:
            return None

    @thread_safe
    def get_uncaptured_screenshots(self):
        db_query = Query()
        result = self.db_orders.search(
            (db_query.status == "processing") & (db_query.stage == "screenshots")
        )
        if result:
            return result
        else:
            return False

    @thread_safe
    def get_unrendered_orders(self):
        db_query = Query()
        result = self.db_orders.search(
            (db_query.stage == "screenshots_captured")
            & (
                (db_query.request_type == "video_auto")
                | (db_query.request_type == "video_files")
            )
            & (db_query.status == "processing")
        )
        if result:
            return result
        else:
            return False

    @thread_safe
    def get_unsent_orders(self):
        db_query = Query()
        result = self.db_orders.search(
            (db_query.stage == "sending") & (db_query.status == "processing")
        )
        if result:
            return result
        else:
            return False

    @thread_safe
    def terminate_all_sessions(self, user_id):
        db_query = Query()
        results = self.db_orders.search(
            (db_query.telegram_id == user_id)
            & ((db_query.status == "active") | (db_query.status == "processing"))
        )
        if results:
            for result in results:
                self.db_orders.update({"status": "user_terminated"}, doc_ids=[result.doc_id])
            return True
        else:
            return False

    @thread_safe
    def start_terminate_all_active_sessions(self):
        db_query = Query()
        results = self.db_orders.search(
            (db_query.status == "active") | (db_query.status == "processing")
        )
        if results:
            for result in results:
                self.db_orders.update(
                    {"status": "restart_terminated"}, doc_ids=[result.doc_id]
                )
            return True
        else:
            return False

    @thread_safe
    def get_request_type(self, user_id):
        doc_id = self.get_active_doc_id(user_id)
        if doc_id:
            query = self.db_orders.get(doc_id=doc_id)
            return query["request_type"]
        else:
            return False

    @thread_safe
    def get_is_user_in_db(self, user_id):
        db_indb_query = Query()
        results = self.db_allowed_users.search((db_indb_query.telegram_id == user_id))
        return True if results else False

    @thread_safe
    def get_is_user_allowed(self, user_id):
        db_allowed_query = Query()
        results = self.db_allowed_users.search(
            (db_allowed_query.telegram_id == user_id)
            & (db_allowed_query.status == "approved")
        )
        if results:
            return True
        else:
            return False

    @thread_safe
    def add_pending_user(self, update):
        if self.get_is_user_in_db(user_id=update.message.from_user.id):
            return False
        else:
            parameters = {
                "first_name": update.message.from_user.first_name,
                "telegram_id": update.message.from_user.id,
                "chat_id": update.message.chat.id,
                "status": "pending",
            }
            self.db_allowed_users.insert(parameters)
            return True

    @thread_safe
    def get_pending_register_requests(self):
        db_query = Query()
        results = self.db_allowed_users.search((db_query.status == "pending"))
        return results if results else False

    @thread_safe
    def get_registered_users(self):
        db_query = Query()
        results = self.db_allowed_users.search((db_query.status == "approved"))
        return results if results else False

    @thread_safe
    def get_blocked_users(self):
        db_query = Query()
        results = self.db_allowed_users.search((db_query.status == "blocked"))
        return results if results else False

    @thread_safe
    def set_user_permission(self, user_id, permission):
        db_query = Query()
        results = self.db_allowed_users.search((db_query.telegram_id == user_id))
        if results:
            if permission:
                self.db_allowed_users.update(
                    {"status": "approved"}, db_query.telegram_id == user_id
                )
                bot.send_message(
                    chat_id=user_id,
                    text="Твой запрос одобрен. Можешь начать работу с ботом через команду /start",
                )
            else:
                self.db_allowed_users.update(
                    {"status": "blocked"}, db_query.telegram_id == user_id
                )
            return True
        else:
            return False

    @thread_safe
    def get_recent_orders(self):
        db_query = Query()
        interval = time.time() - interlinks.recent_orders_interval_hours * 360
        results = self.db_orders.search((db_query.start_timestamp > interval))
        return results

    @thread_safe
    def get_processing_orders(self):
        db_query = Query()
        results = self.db_orders.search((db_query.status == "processing"))
        return results

    @thread_safe
    def get_active_orders(self):
        db_query = Query()
        results = self.db_orders.search(
            (db_query.status == "active") | (db_query.status == "processing")
        )
        return results


    # sys_events db
    @thread_safe
    def log_event(self, type, description):
        return self.db_sys_events.insert({
            'type': type,
            'timestamp': time.time(),
            'description': description,
        })


    @thread_safe
    def log_error(self, description):
        return self.log_event('error', description)


    @thread_safe
    def get_errors(self, description):
        db_query = Query()
        return self.db_sys_events.search((db_query.type == 'error') & (db_query.description == description))


    @thread_safe
    def get_latest_launch_time(self):
        db_query = Query()
        results = self.db_sys_events.search((db_query.type == 'run') & (db_query.description == 'bot_launch'))
        try:
            return results[-1]['timestamp']
        except IndexError:
            return False


    @thread_safe
    def get_today_orders(self, only_count: bool = False) -> list[Document]:
        today_obj = datetime.datetime.today().today()
        today_ts = today_obj.replace(hour=0, minute=0, second=0, microsecond=0).timestamp()
        
        tomorrow_obj = today_obj + datetime.timedelta(days=1)
        tomorrow_ts = tomorrow_obj.timestamp()

        db_query = Query()
        results = self.db_orders.search(
            (db_query.start_timestamp < tomorrow_ts) & (db_query.start_timestamp > today_ts)
        )

        return len(results) if only_count else results



db_handler = TinyDBHandler()
