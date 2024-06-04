from shared.queue_manager.queue_manager import QueueManager
from shared.models.operator_results import OperatorResults, OperatorOutputFile
import time
from io import BytesIO
from secrets import token_hex


def test_queue_manager():
    qm = QueueManager(operator)
    print(qm.append({"order_details": "Order 1"}))
    print(qm._queue)
    print(qm._processing)
    print(qm.append({"order_details": "Order 2"}))

    print(qm.append({"order_details": "Order 3"}))

    print(qm._queue)
    print(qm._processing)

    qm.start_processing()
    # qm.append("Order 4")
    # qm.append("Order 5")
    # qm.append("Order 6")
    # qm.append("Order 7")
    # qm.append("Order 8")
    # qm.append("Order 9")
    # qm.append("Order 10")
    # qm.start_processing(print)


def operator(item: dict) -> OperatorResults:
    output_files = [
        OperatorOutputFile(content=BytesIO(), filename=token_hex(6) + ".img") for _ in range(2)
    ]
    results = OperatorResults(
        operator_output=output_files, success=True, error=False, error_message=""
    )
    time.sleep(3)
    return results
