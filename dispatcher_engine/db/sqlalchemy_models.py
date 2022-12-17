from typing import List, Optional
from sqlalchemy import ForeignKey, Integer, Sequence, BigInteger
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    DeclarativeBase,
    relationship,
)
import textwrap


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    first_name: Mapped[Optional[str]]
    description: Mapped[Optional[str]]

    status: Mapped[Optional[str]]

    current_stage: Mapped[Optional[str]]  # no idea what i created this for

    user_id: Mapped[int] = mapped_column(
        "user_id", Integer, Sequence("user_id_seq"), primary_key=True
    )
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True)

    chat_id: Mapped[Optional[int]]
    orders: Mapped[List["Order"]] = relationship(
        # "Order",
        # backref="user",
        back_populates="user",
        # default_factory=list,
    )

    def __repr__(self) -> str:
        return textwrap.dedent(
            f"""User(ID: {self.user_id}
                First Name: {self.first_name}
                Telegram ID: {self.telegram_id}
                Status: {self.status})"""
        )


class Order(Base):
    __tablename__ = "orders"

    # main description
    status: Mapped[Optional[str]]
    request_type: Mapped[Optional[str]]

    order_start_timestamp: Mapped[Optional[int]]
    order_creation_end_timestamp: Mapped[Optional[int]]

    stage: Mapped[Optional[str]]
    link: Mapped[Optional[str]]

    # screenshots / static images
    screenshots_ready: Mapped[Optional[bool]]
    link_type: Mapped[Optional[str]]

    # video description
    fg_enabled: Mapped[Optional[bool]]
    bg_path: Mapped[Optional[str]]
    fg_path: Mapped[Optional[str]]
    bg_animation: Mapped[Optional[str]]
    fg_animation: Mapped[Optional[str]]

    video_ready: Mapped[Optional[bool]]
    render_output_path: Mapped[Optional[str]]
    audio_enabled: Mapped[Optional[bool]]
    audio_path: Mapped[Optional[str]]

    quote_enabled: Mapped[Optional[bool]]
    quote_text: Mapped[Optional[str]]
    quote_author_enabled: Mapped[Optional[bool]]
    quote_author_text: Mapped[Optional[str]]

    # readtime
    readtime_result: Mapped[Optional[str]]
    readtime_speed: Mapped[Optional[int]]
    readtime_text: Mapped[Optional[str]]

    # results
    results_message: Mapped[Optional[str]]

    # id section
    order_id: Mapped[int] = mapped_column(
        "order_id", Integer, Sequence("order_id_seq"), primary_key=True
    )
    # relationship
    user_telegram_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.telegram_id")
    )

    user: Mapped["User"] = relationship(back_populates="orders")
    
    user_first_name:Mapped[Optional[str]]

    def __repr__(self) -> str:
        return textwrap.dedent(
            f"""Order(ID: {self.order_id}
                Status: {self.status}
                Request Type: {self.request_type}
                Start Time: {self.order_start_timestamp})"""
        )


class SystemEventLog(Base):
    __tablename__ = "system_events"
    sysevent_id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str]
    description: Mapped[str]
    timestamp: Mapped[int]
