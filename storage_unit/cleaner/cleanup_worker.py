import time

from cleaner.helpers.asset_eraser import erase_order_assets
from cleaner.helpers.fetch_orders import fetch_all_active_orders
from cleaner.helpers.order_classifier import should_order_retire

ORDER_MAX_AGE_HOURS = 7


def expiry_asset_cleaner() -> None:
    while True:
        print("cleaner working every hour.")
        time.sleep(60 * 60)

        active_orders = fetch_all_active_orders()
        if not active_orders:
            continue

        for order in active_orders:
            if should_order_retire(order, ORDER_MAX_AGE_HOURS):
                erase_order_assets(order)
