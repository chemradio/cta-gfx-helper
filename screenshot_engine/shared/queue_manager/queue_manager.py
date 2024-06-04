from collections import deque
from threading import Thread
from time import perf_counter
from shared.database.db import DBHandler
import uuid
from pathlib import Path
from typing import Callable
from shared.models.operator_results import OperatorResults, OperatorOutputFile


class QueueManager:
    def __init__(self, operator: Callable[[dict], OperatorResults]):
        self._queue = deque()
        self._processing = False
        self._operator = operator

    def append(self, item: dict):
        order_id = str(uuid.uuid4())
        item.update({"order_id": order_id})
        DBHandler.insert(item)
        self._queue.append(item)
        return order_id

    def start_processing(self):
        if self._processing:
            print(
                f"Already processing queue. Continue... Queue length: {len(self._queue)+1}"
            )
            return
        thread = Thread(target=self._process_queue)
        thread.start()
        thread.join()

    def _process_queue(self):
        print("Start processing queue")
        self._processing = True

        queue_start = perf_counter()
        while self._queue:
            print(f"Queue length: {len(self._queue)}")
            item: dict = self._queue.popleft()
            print(f"Processing queue item: {item}")
            task_start = perf_counter()

            operator_results = self._operator(item)

            update_data = dict()

            if operator_results.error:
                print(f"Error processing item: {operator_results.error_message}")
                update_data.update(
                    {
                        "error": True,
                        "error_message": operator_results.error_message,
                    },
                )

            if operator_results.success and operator_results.operator_output:
                self._store_operator_output(operator_results.operator_output)
                update_data.update(
                    {
                        "output_filenames": [
                            output.filename
                            for output in operator_results.operator_output
                        ]
                    }
                )

            DBHandler.update(item["order_id"], {"status": "finished", **update_data})

            task_stop = perf_counter()
            print("Done processing item")
            print(f"Item processing took {task_stop - task_start} seconds to complete")

        else:
            print("Queue is empty. Stopping...")
            self._processing = False

        queue_stop = perf_counter()
        print(f"Queue processing took {queue_stop - queue_start} seconds to complete")

    def _store_operator_output(
        self,
        operator_output: list[OperatorOutputFile],
        store_folder: Path = Path.cwd() / "storage",
    ) -> None:
        for output in operator_output:
            file_path = store_folder / output.filename
            with open(file_path, "wb") as file:
                file.write(output.content.getvalue())

    def __str__(self) -> str:
        return str(self._queue)
