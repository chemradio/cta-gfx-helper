from db_mongo import Orders


def is_admin_terminated(order: dict) -> bool:
    return Orders.find_one({"order_id": order["order_id"]}).get(
        "admin_terminated", False
    )


class AdminTerminatedException(Exception):
    def __init__(self, message="Administrator has terminated the order"):
        super().__init__(message)
