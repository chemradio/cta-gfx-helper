from py_gfxhelper_lib import QueueManager
import uuid
from datetime import datetime, timedelta
import random
import asyncio


async def update_cookies(queue: QueueManager) -> None:
    websites = [
        "https://facebook.com",
        "https://instagram.com",
        "https://x.com",
    ]
    for website in websites:
        queue.append(
            {
                "order_id": str(uuid.uuid4()),
                "screenshot_link": website,
                "callback_url": None,
                "status": "new",
                "no_store_output": True,
            }
        )
    queue.start_processing()


async def schedule_cookie_update(queue: QueueManager):
    while True:
        now = datetime.now()
        target_time = datetime.combine(now.date(), datetime.min.time()) + timedelta(
            seconds=random.randint(0, 8 * 3600)
        )
        if target_time < now:  # If the random time for today is in the past
            target_time += timedelta(days=1)
        delay = (target_time - now).total_seconds()
        print(f"Task scheduled at {target_time}")

        # Wait until the scheduled time
        await asyncio.sleep(delay)
        await update_cookies(queue)
        await asyncio.sleep(5 * 60)
