import os
from typing import Optional
import config
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from db.sqlalchemy_models import Base, User, Order


class SQLHandler:
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(SQLHandler, cls).__new__(cls)
        return cls.instance

    def __init__(self) -> None:
        self.engine = create_engine(
            config.POSTGRES_URL,
            echo=True,
            future=True,
        )
        self.Session = sessionmaker(self.engine)
        self.base = Base
        self.base.metadata.create_all(bind=self.engine)


    def re_init_full_truncate(self) -> None:
        self.recreate_tables()


    def init_add_admin(self) -> None:
        admin_telegram_id = os.environ.get("BOT_ADMIN")
        print(f"{admin_telegram_id=}")
        with self.Session() as session:
            admin = User(
                first_name="admin",
                status="admin",
                telegram_id=admin_telegram_id,
                chat_id=admin_telegram_id,
            )
            session.add(admin)
            session.commit()

    def recreate_tables(self) -> None:
        self.base.metadata.drop_all(bind=self.engine)
        self.base.metadata.create_all(bind=self.engine)

    def truncate_orders(self) -> None:
        self.base.metadata.drop_all(bind=self.engine, tables=[Order.__table__])
        self.base.metadata.create_all(bind=self.engine, tables=[Order.__table__])

    def add_order(self, **kwargs) -> Order:
        user_telegram_id = kwargs.pop("telegram_id")
        print(f"{__name__}:{user_telegram_id=}")
        user = self.find_user_by_telegram_id(user_telegram_id)
        print(f"{__name__}:{user=}")
        print(f"{__name__}:{user.telegram_id=}")

        with self.Session() as session:
            order = Order(**kwargs, user=user, user_telegram_id=user.telegram_id)
            session.add(order)
            session.commit()
            return order.order_id

    def add_user(self, **kwargs) -> User:
        with self.Session() as session:
            user = User(**kwargs)
            session.add(user)
            session.commit()
            return user  # .user_id

    def edit_user(self, telegram_id: int, **kwargs) -> Optional[User]:
        with self.Session() as session:
            stmt = select(User).where(User.telegram_id == telegram_id)
            results = session.scalars(stmt).all()
            if not results:
                return None

            user = results[0]
            for key, value in kwargs.items():
                setattr(user, key, value)
            session.commit()
            return user

    def edit_order(self, order_id: int, **kwargs) -> Optional[Order]:
        with self.Session() as session:
            stmt = select(Order).where(Order.order_id == order_id)
            results = session.scalars(stmt).all()
            if not results:
                return None

            order = results[0]
            for key, value in kwargs.items():
                setattr(order, key, value)
            session.commit()
            return order

    def list_users(self, type: str = None) -> list:
        with self.Session() as session:
            if type:
                query = select(User).where(User.status == type)
            else:
                query = select(User)
            results = session.scalars(query).all()
            return results if results else []

    def list_orders(self, type: str=None) -> list:
        with self.Session() as session:
            if type:
                # to be developed. Order.status - not correct
                query = select(Order).where(Order.status == type)
            else:
                query = select(Order)
            results = session.scalars(query).all()
            return results if results else []

    def find_user_by_telegram_id(self, telegram_id: int) -> Optional[User]:
        with self.Session() as session:
            query = select(User).where(User.telegram_id == telegram_id)
            results = session.scalars(query).all()
            return results[0] if results else None

    # def update_doc_db_parameters(self, order_id, parameters: dict):
    #     parameters = self.deprecation_process_parameters(parameters)
    #     if not order_id:
    #         return None
    #     with self.Session() as session:
    #         order = session.query(Order).get(order_id)
    #         for key, value in parameters.items():
    #             setattr(order, key, value)
    #     return True

    # def get_uncaptured_screenshots(self):
    #     with self.Session() as session:
    #         query = select(Order).where(
    #             and_(Order.status == "processing", Order.stage == "screenshots")
    #         )
    #         results = session.scalars(query).all()
    #     return results if results else None

    # def get_unrendered_videos(self):
    #     with self.Session() as session:
    #         query = select(Order).where(
    #             and_(
    #                 Order.stage == "screenshots_captured",
    #                 Order.status == "processing",
    #                 Order.request_type.in_(["video_auto", "video_files"]),
    #             )
    #         )
    #         results = session.scalars(query).all()
    #     return results if results else None

    # def get_unsent_orders(self):
    #     with self.Session() as session:
    #         query = select(Order).where(
    #             and_(Order.stage == "sending", Order.status == "processing")
    #         )
    #         results = session.scalars(query).all()
    #     return results if results else None

    # def terminate_all_sessions(self, user_id):
    #     with self.Session() as session:
    #         query = (
    #             select(Order)
    #             .join(User, Order.user)
    #             .where(
    #                 and_(
    #                     User.telegram_id == user_id,
    #                     or_(Order.status == "active", Order.status == "processing"),
    #                 )
    #             )
    #         )

    #         results = session.scalars(query).all()
    #         if not results:
    #             return None

    #         for order in results:
    #             order.status == "user_terminated"
    #         session.commit()
    #         return True

    # def start_terminate_all_active_sessions(self):
    #     with self.Session() as session:
    #         query = select(Order).where(
    #             or_(Order.status == "active", Order.status == "processing")
    #         )

    #         results = session.scalars(query).all()
    #         if not results:
    #             return None

    #         for order in results:
    #             order.status == "restart_termintated"
    #         session.commit()
    #     return True

    def get_is_user_in_db(self, user_id):
        with self.Session() as session:
            query = select(User).where(User.telegram_id == user_id)
            results = session.scalars(query).all()
        return True if results else False

    # def get_is_user_allowed(self, user_id):
    #     with self.Session() as session:
    #         query = select(User).where(
    #             and_(User.telegram_id == user_id, User.status == "approved")
    #         )
    #         results = session.scalars(query).all()
    #     return True if results else False

    # def add_pending_user(self, update):
    #     if self.get_is_user_in_db(user_id=update.message.from_user.id):
    #         return False

    #     parameters = {
    #         "first_name": update.message.from_user.first_name,
    #         "telegram_id": update.message.from_user.id,
    #         "chat_id": update.message.chat.id,
    #         "status": "pending",
    #     }
    #     with self.Session() as session:
    #         user = User(**parameters)
    #         session.add(user)
    #         session.commit()

    #     return True

    # def get_pending_register_requests(self):
    #     with self.Session() as session:
    #         query = select(User).where(User.status == "pending")
    #         results = session.scalars(query).all()
    #     return results if results else False

    # def get_blocked_users(self):
    #     with self.Session() as session:
    #         query = select(User).where(User.status == "blocked")
    #         results = session.scalars(query).all()
    #     return results if results else False

    # def set_user_permission(self, user_id, permission):
    #     with self.Session() as session:
    #         query = select(User).where(User.telegram_id == user_id)
    #         results = session.scalars(query).all()

    #         if not results:
    #             return False

    #         user = results[0]
    #         if permission:
    #             user.status = "approved"
    #         else:
    #             user.status = "blocked"
    #         session.commit()
    #     return True

    # def get_recent_orders(self):
    #     with self.Session() as session:
    #         now = datetime.now()
    #         limit = now - timedelta(config.RECENT_ORDERS_INTERVAL_HOURS)
    #         query = select(Order).where(Order.start_timestamp > limit)
    #         results = session.scalars(query).all()
    #     return results

    # def get_processing_orders(self):
    #     with self.Session() as session:
    #         query = select(Order).where(Order.status == "processing")
    #         results = session.scalars(query).all()
    #     return results

    # def get_active_orders(self):
    #     with self.Session() as session:
    #         query = select(Order).where(
    #             or_(Order.status == "processing", Order.status == "active")
    #         )
    #         results = session.scalars(query).all()
    #     return results

    # # sys_events db
    # def log_event(self, type, description):
    #     with self.Session() as session:
    #         event = SystemEventLog(
    #             type=type, description=description, timestamp=datetime.now()
    #         )
    #         session.add(event)
    #         session.commit()

    # def log_error(self, description):
    #     return self.log_event("error", description)

    # def get_errors(self, description):
    #     with self.Session() as session:
    #         query = select(SystemEventLog).where(
    #             and_(
    #                 SystemEventLog.type == "error",
    #                 SystemEventLog.description == description,
    #             )
    #         )
    #         results = session.scalars(query)
    #     return results

    # def get_latest_launch_time(self):
    #     with self.Session() as session:
    #         query = select(SystemEventLog).where(
    #             and_(
    #                 SystemEventLog.type == "run",
    #                 SystemEventLog.description == "bot_launch",
    #             )
    #         )
    #         results = session.scalars(query)
    #     return results[-1].timestamp.timestamp

    # def get_today_orders(self, only_count: bool = False) -> list:
    #     today_start = datetime.today().replace(
    #         hour=0, minute=0, second=0, microsecond=0
    #     )
    #     with self.Session() as session:
    #         query = select(Order).where(Order.start_timestamp > today_start)
    #         results = session.scalars(query).all()

    #     return len(results) if only_count else results
