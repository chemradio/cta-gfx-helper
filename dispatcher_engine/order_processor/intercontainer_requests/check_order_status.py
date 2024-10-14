import time

import requests


def check_order_status(order_id: str, container_url: str) -> dict:
    r = requests.get(container_url, json={"order_id": order_id})
    return r.json()


def poll_order_status_finished(order_id: str, container_url: str) -> dict:
    while True:
        order_status = check_order_status(order_id, container_url)
        if order_status["status"] == "finished":
            return order_status
        time.sleep(3)
