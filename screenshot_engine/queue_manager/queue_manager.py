from collections import deque
from threading import Thread
from time import perf_counter


class QueueManager:
    def __init__(self):
        self._queue = deque()
        self._processing = False

    def append(self, item):
        self._queue.append(item)

    def start_processing(self, operator: callable):
        if self._processing:
            print(
                f"Already processing queue. Continue... Queue length: {len(self._queue)+1}"
            )
            return
        Thread(target=self._process_queue, args=(operator,)).start()

    def _process_queue(self, operator: callable):
        print("Start processing queue")
        self._processing = True

        queue_start = perf_counter()
        while self._queue:
            print(f"Queue length: {len(self._queue)}")
            item = self._queue.popleft()
            print(f"Processing queue item: {item}")
            task_start = perf_counter()
            operator(item)
            task_stop = perf_counter()
            print("Done processing item")
            print(f"Item processing took {task_stop - task_start} seconds to complete")

        else:
            print("Queue is empty. Stopping...")
            self._processing = False

        queue_stop = perf_counter()
        print(f"Queue processing took {queue_stop - queue_start} seconds to complete")

    def __str__(self) -> str:
        return str(self._queue)
