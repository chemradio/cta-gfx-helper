import requests


def notify_dispatcher(dispatcher_url: str, notification: dict):
    requests.post(dispatcher_url, json=notification)
