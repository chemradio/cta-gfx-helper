import threading
from functools import wraps
import tinydb


db_lock = threading.RLock()


def thread_safe(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Acquire the lock
        with db_lock:
            # Call the original function
            result = func(*args, **kwargs)
        return result

    return wrapper


class DBHandler:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        self.db = tinydb.TinyDB("db.json")
        self.drop()

    @thread_safe
    def drop(self):
        self.db.truncate()

    @thread_safe
    def all(self):
        return self.db.all()

    @thread_safe
    def get_order(self, order_id: str | None = None, doc_id: int | None = None):
        if order_id:
            return self.db.get(tinydb.Query().order_id == order_id)
        elif doc_id:
            return self.db.get(doc_id=doc_id)
        else:
            return None

    @thread_safe
    def insert(self, data: dict):
        doc_id = self.db.insert(data)
        return self.get_order(doc_id=doc_id)

    @thread_safe
    def update(self, order_id: str, data: dict):
        self.db.update(data, tinydb.Query().order_id == order_id)
        return self.get_order(order_id=order_id)

    @thread_safe
    def delete(self, order_id: str) -> None:
        self.db.remove(tinydb.Query().order_id == order_id)
        return None

    @thread_safe
    def get_oldest_new_order(self):
        result = self.db.search((tinydb.Query().status == "NEW"))
        if result:
            return sorted(result, key=lambda x: x["created"])[0]
        else:
            return None



db_handler = DBHandler()