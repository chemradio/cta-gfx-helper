import json
import os
from datetime import datetime, timedelta
from sqlalchemy import create_engine, select, and_, or_
from sqlalchemy.orm import sessionmaker
from .table_descriptions import Base, SystemEventLog, User, Order


def timestamp_to_datetime(timestamp: int | float):
    return datetime.fromtimestamp(timestamp)


class SQLHandler:
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(SQLHandler, cls).__new__(cls)
        return cls.instance

    def __init__(self) -> None:
        connection_string = str()
        if interlinks.USE_SQLITE:
            connection_string = f"sqlite:///{interlinks.SQLITE_PATH}"

        self.engine = create_engine(
            connection_string,
            # echo=True,
            future=True,
        )
        self.Session = sessionmaker(self.engine)

        if not os.path.exists(interlinks.SQLITE_PATH):
            create_sqlite_file()
            Base.metadata.create_all(self.engine)
            self.import_users_from_tinydb()

    def add_db_entry(self, parameters: dict) -> Order:
        parameters = self.deprecation_process_parameters(parameters)

        with self.Session() as session:
            order = Order(**parameters)
            session.add(order)
            session.commit()
        return order

    def get_init_status(self, user_id: int):
        with self.Session() as session:
            query = (
                select(Order)
                .join(User, Order.user)
                .where(and_(Order.status == "init", User.telegram_id == user_id))
            )
            results = session.scalars(query).all()
            if not results:
                return False

            # terminate previous active sessions
            if len(results) > 1:
                for i in range(len(results) - 1):
                    bad_order = session.query(Order).get(results[i].order_id)
                    bad_order.status = "error_terminated"
                session.commit()
            return results[-1].order_id

    def activate_init_status(self, user_id):
        order_id = self.get_init_status(user_id=user_id)
        if order_id:
            with self.Session() as session:
                order = session.query(Order).get(order_id)
                order.status = "active"
                session.commit()

    def get_active_doc_id(self, user_id):
        with self.Session() as session:
            query = (
                select(Order)
                .join(User, Order.user)
                .where(and_(Order.status == "active", User.telegram_id == user_id))
            )
            results = session.scalars(query).all()
            if not results:
                return None

            # terminate previous active sessions
            if len(results) > 1:
                for i in range(len(results) - 1):
                    bad_order = session.query(Order).get(results[i].order_id)
                    bad_order.status = "error_terminated"
                session.commit()
            return results[-1].order_id

    def get_current_stage(self, user_id):
        order_id = self.get_active_order_id(user_id)
        if not order_id:
            return None

        with self.Session() as session:
            order = session.query(Order).get(order_id)
            return order.stage

    def set_user_stage(self, user_id, stage):
        order_id = self.get_active_order_id(user_id)
        if not order_id:
            return None

        with self.Session() as session:
            order = session.query(Order).get(order_id)
            order.stage = stage
            session.commit()
        return True

    def update_db_parameters(self, user_id, parameters: dict):
        parameters = self.deprecation_process_parameters(parameters)
        order_id = self.get_active_order_id(user_id)

        if not order_id:
            return None
        with self.Session() as session:
            order = session.query(Order).get(order_id)
            for key, value in parameters.items():
                setattr(order, key, value)
            session.commit()
        return True

    def update_doc_db_parameters(self, order_id, parameters: dict):
        parameters = self.deprecation_process_parameters(parameters)
        if not order_id:
            return None
        with self.Session() as session:
            order = session.query(Order).get(order_id)
            for key, value in parameters.items():
                setattr(order, key, value)
        return True

    def get_active_entry_data(self, user_id):
        active_order_id = self.get_active_order_id(user_id)
        with self.Session() as session:
            order = session.query(Order).get(active_order_id)
        return order if order else None

    def get_unchecked_quotes(self):
        with self.Session() as session:
            query = select(Order).where(Order.stage == "check_quote")
            results = session.scalars(query).all()
        return results if results else None

    def get_uncaptured_screenshots(self):
        with self.Session() as session:
            query = select(Order).where(
                and_(Order.status == "processing", Order.stage == "screenshots")
            )
            results = session.scalars(query).all()

        return results if results else None

    def get_unrendered_orders(self):
        with self.Session() as session:
            query = select(Order).where(
                and_(
                    Order.stage == "screenshots_captured",
                    Order.status == "processing",
                    Order.request_type.in_(["video_auto", "video_files"]),
                )
            )
            results = session.scalars(query).all()

        return results if results else None

    def get_unsent_orders(self):
        with self.Session() as session:
            query = select(Order).where(
                and_(Order.stage == "sending", Order.status == "processing")
            )
            results = session.scalars(query).all()
        return results if results else None

    def terminate_all_sessions(self, user_id):
        with self.Session() as session:
            query = (
                select(Order)
                .join(User, Order.user)
                .where(
                    and_(
                        User.telegram_id == user_id,
                        or_(Order.status == "active", Order.status == "processing"),
                    )
                )
            )

            results = session.scalars(query).all()
            if not results:
                return None

            for order in results:
                order.status == "user_terminated"
            session.commit()
            return True

    def start_terminate_all_active_sessions(self):
        with self.Session() as session:
            query = select(Order).where(
                or_(Order.status == "active", Order.status == "processing")
            )

            results = session.scalars(query).all()
            if not results:
                return None

            for order in results:
                order.status == "restart_termintated"
            session.commit()
        return True

    def get_request_type(self, user_id):
        with self.Session() as session:
            order_id = self.get_active_order_id(user_id)
            if not order_id:
                return False

            order = session.query(Order).get(order_id)
            return order.request_type

    def get_is_user_in_db(self, user_id):
        with self.Session() as session:
            query = select(User).where(User.telegram_id == user_id)
            results = session.scalars(query).all()
        return True if results else False

    def get_is_user_allowed(self, user_id):
        with self.Session() as session:
            query = select(User).where(
                and_(User.telegram_id == user_id, User.status == "approved")
            )
            results = session.scalars(query).all()
        return True if results else False

    def add_pending_user(self, update):
        if self.get_is_user_in_db(user_id=update.message.from_user.id):
            return False

        parameters = {
            "first_name": update.message.from_user.first_name,
            "telegram_id": update.message.from_user.id,
            "chat_id": update.message.chat.id,
            "status": "pending",
        }
        with self.Session() as session:
            user = User(**parameters)
            session.add(user)
            session.commit()

        return True

    def get_pending_register_requests(self):
        with self.Session() as session:
            query = select(User).where(User.status == "pending")
            results = session.scalars(query).all()
        return results if results else False

    def get_registered_users(self):
        with self.Session() as session:
            query = select(User).where(User.status == "approved")
            results = session.scalars(query).all()
        return results if results else False

    def get_blocked_users(self):
        with self.Session() as session:
            query = select(User).where(User.status == "blocked")
            results = session.scalars(query).all()
        return results if results else False

    def set_user_permission(self, user_id, permission):
        with self.Session() as session:
            query = select(User).where(User.telegram_id == user_id)
            results = session.scalars(query).all()

            if not results:
                return False

            user = results[0]
            if permission:
                user.status = "approved"
                # bot.send_message(
                #     chat_id=user_id,
                #     text="Твой запрос одобрен. Можешь начать работу с ботом через команду /start",
                # )
            else:
                user.status = "blocked"
            session.commit()
        return True

    def get_recent_orders(self):
        with self.Session() as session:
            now = datetime.now()
            limit = now - timedelta(interlinks.RECENT_ORDERS_INTERVAL_HOURS)
            query = select(Order).where(Order.start_timestamp > limit)
            results = session.scalars(query).all()
        return results

    def get_processing_orders(self):
        with self.Session() as session:
            query = select(Order).where(Order.status == "processing")
            results = session.scalars(query).all()
        return results

    def get_active_orders(self):
        with self.Session() as session:
            query = select(Order).where(
                or_(Order.status == "processing", Order.status == "active")
            )
            results = session.scalars(query).all()
        return results

    # import from tinyDB
    def import_users_from_tinydb(
        self, users_db: str = "./config_and_db/db_allowed_users.json"
    ) -> None:
        users = list()
        with open(users_db, "r") as f:
            data: dict = json.load(f)["_default"]

            for entry in data.values():
                users.append(User(**entry))

        with self.Session() as session:
            for user in users:
                try:
                    session.add(user)
                    session.commit()
                except:
                    print(f"Failed to import user: {user}")

    # @thread_safe
    # def import_orders_from_tinydb(self, orders_db: str='./config_and_db/db_orders.json') -> None:
    #     orders = list()
    #     with open(orders_db, 'r') as f:
    #         data: dict = json.load(f)['_default']

    #         for entry in data.values():
    #             orders.append(Order(**entry))

    #     with self.Session() as session:
    #         session.add_all(orders)
    #         session.commit()

    # sys_events db
    def log_event(self, type, description):
        with self.Session() as session:
            event = SystemEventLog(
                type=type, description=description, timestamp=datetime.now()
            )
            session.add(event)
            session.commit()

    def log_error(self, description):
        return self.log_event("error", description)

    def get_errors(self, description):
        with self.Session() as session:
            query = select(SystemEventLog).where(
                and_(
                    SystemEventLog.type == "error",
                    SystemEventLog.description == description,
                )
            )
            results = session.scalars(query)
        return results

    def get_latest_launch_time(self):
        with self.Session() as session:
            query = select(SystemEventLog).where(
                and_(
                    SystemEventLog.type == "run",
                    SystemEventLog.description == "bot_launch",
                )
            )
            results = session.scalars(query)
        return results[-1].timestamp.timestamp

    def get_today_orders(self, only_count: bool = False) -> list:
        today_start = datetime.today().replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        with self.Session() as session:
            query = select(Order).where(Order.start_timestamp > today_start)
            results = session.scalars(query).all()

        return len(results) if only_count else results

    def find_convert_timestamps_datetime(self, parameters: dict) -> dict:
        # DEPRECATION NOTICE!!!
        # convert old style epoch to datetime first
        # following stick lines to be deprecated
        # Only valid for hybrid or TinyDB obly operation
        queue = {
            "start_timestamp": parameters.get("start_timestamp"),
            "start_render_timestamp": parameters.get("start_render_timestamp"),
        }
        for timestamp_name, timestamp in queue.items():
            if isinstance(timestamp, datetime) or (timestamp is None):
                continue
            converted_timestamp = datetime.fromtimestamp(timestamp)
            parameters[timestamp_name] = converted_timestamp
        return parameters

    def find_convert_user(self, parameters: dict) -> dict:
        # DEPRECATION NOTICE!!!
        telegram_id = parameters.get("telegram_id")
        pop_fields = ("telegram_id", "first_name", "chat_id")
        for field in pop_fields:
            parameters.pop(field)
        if not telegram_id:
            return parameters

        with self.Session() as session:
            query = select(User).where(User.telegram_id == telegram_id)
            user = session.scalars(query).all()[0]
        parameters["user"] = user
        parameters["user_id"] = user.user_id
        return parameters

    def deprecation_process_parameters(self, parameters: dict) -> dict:
        parameters = self.find_convert_timestamps_datetime(parameters)
        parameters = self.find_convert_user(parameters)
        return parameters
