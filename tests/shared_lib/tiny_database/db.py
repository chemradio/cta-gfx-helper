import functools
import threading

import tinydb

db_lock = threading.RLock()


def thread_safe(function):
    def wrapper(*args, **kwargs):
        with db_lock:
            # Call the original function
            return function(*args, **kwargs)

    return functools.update_wrapper(wrapper, function)


class DBHandler:
    db = tinydb.TinyDB("db.json")
    db.truncate()

    @classmethod
    @thread_safe
    def drop(cls):
        cls.db.truncate()

    @classmethod
    @thread_safe
    def all(cls):
        return cls.db.all()

    @classmethod
    @thread_safe
    def get_order(cls, order_id: str | None = None, doc_id: int | None = None):
        if order_id:
            return cls.db.get(tinydb.Query().order_id == order_id)
        elif doc_id:
            return cls.db.get(doc_id=doc_id)
        else:
            return None

    @classmethod
    @thread_safe
    def insert(cls, data: dict):
        doc_id = cls.db.insert(data)
        return cls.get_order(doc_id=doc_id)

    @classmethod
    @thread_safe
    def update(cls, order_id: str, data: dict):
        cls.db.update(data, tinydb.Query().order_id == order_id)
        return cls.get_order(order_id=order_id)

    @classmethod
    @thread_safe
    def delete(cls, order_id: str) -> None:
        cls.db.remove(tinydb.Query().order_id == order_id)
        return None

    @classmethod
    @thread_safe
    def get_oldest_new_order(cls):
        result = cls.db.search((tinydb.Query().status == "NEW"))
        if result:
            return sorted(result, key=lambda x: x["created"])[0]
        else:
            return None
