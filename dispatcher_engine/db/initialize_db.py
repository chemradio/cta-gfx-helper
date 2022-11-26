from db.sql_handler import SQLHandler


def initialize_db() -> SQLHandler:
    db_handler = SQLHandler()
    return db_handler
