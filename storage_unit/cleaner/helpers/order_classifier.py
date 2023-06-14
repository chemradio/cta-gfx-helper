from datetime import datetime, timedelta


def should_order_retire(order, ORDER_MAX_AGE_HOURS: int = 7) -> bool:
    ORDER_MAX_AGE_SECONDS = ORDER_MAX_AGE_HOURS * 60 * 60
    order_time: timedelta = order.order_creation_end_timestamp
    current_time = datetime.now()
    order_age_seconds = (current_time - order_time).total_seconds()
    return order_age_seconds > ORDER_MAX_AGE_SECONDS
