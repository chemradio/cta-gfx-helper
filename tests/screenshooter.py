import httpx


SINGLE_SCREENSHOT_URLS = [
    "https://www.google.com",
    "https://www.theverge.com",
    "https://www.ign.com",
]


DUAL_SCREENSHOT_URLS = [
    "https://x.com/elonmusk/status/1860215001157660702",
    "https://t.me/durov/372",
    "https://vk.com/kvovka?w=wall141291173_32875",
    "https://www.instagram.com/p/DAzDZ1-RCTB/",
    "https://www.facebook.com/4/posts/10103996712572761/",
]


def order_screenshots(urls: list[str]) -> list[str]:
    order_ids = []
    with httpx.Client() as client:
        for url in urls:
            response = client.post(
                "http://127.0.0.1:9002/", json={"screenshot_link": url}
            )
            order_ids.append(response.json()["order_id"])

        return order_ids
