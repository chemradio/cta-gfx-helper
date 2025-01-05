from collections import deque
from pathlib import Path
from threading import Thread
from time import perf_counter
from typing import Callable

from ..tiny_database.db import DBHandler
from ..files.asset_file import AssetFile
from ..custom_types.operator_results import OperatorResults


class QueueManager:
    def __init__(
        self,
        storage_path: Path,
        dispatcher_url: str,
        operator: Callable[[dict, dict], OperatorResults],
        db_handler: DBHandler,
        **operator_kwargs,
    ):
        self._queue = deque()
        self._processing = False
        self._storage_path = storage_path
        self._dispatcher_url = dispatcher_url
        self._operator: Callable[[dict, dict], OperatorResults] = operator
        self._operator_kwargs = operator_kwargs
        self._db_handler = db_handler

    def append(self, item: dict) -> None:
        self._db_handler.insert(
            {
                # duplicate the dict except if the value is an UploadFile, then just store the filename
                key: value if not isinstance(value, AssetFile) else value.filename
                for key, value in item.items()
            }
        )

        self._queue.append(item)

    def start_processing(self) -> None:
        if self._processing:
            return
        thread = Thread(target=self._process_queue)
        thread.start()

    def _process_queue(self):
        self._processing = True

        queue_start = perf_counter()
        while self._queue:
            item: dict = self._queue.popleft()
            self._db_handler.update(item["order_id"], {"status": "processing"})
            task_start = perf_counter()

            operator_results = self._operator(item, **self._operator_kwargs)

            update_data = dict()

            if operator_results.error:
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
                        ],
                    }
                )

            self._db_handler.update(
                item["order_id"], {"status": "finished", **update_data}
            )

            task_stop = perf_counter()

        else:
            self._processing = False

        queue_stop = perf_counter()

    def _store_operator_output(
        self,
        operator_output: list[AssetFile],
    ) -> None:
        for output in operator_output:
            file_path = self._storage_path / output.filename
            with open(file_path, "wb") as file:
                file.write(output.bytesio.getvalue())

    def __str__(self) -> str:
        return str(self._queue)
