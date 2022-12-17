DISPATCHER_NODE_HOSTNAME = "dispatcher"
DISPATCHER_NODE_PORT = 9000
DISPATCHER_NODE_URL = f"http://{DISPATCHER_NODE_HOSTNAME}:{DISPATCHER_NODE_PORT}"

LIST_ORDERS_ENDPOINT = f"{DISPATCHER_NODE_URL}/orders/list"
EDIT_ORDER_ENDPOINT = f"{DISPATCHER_NODE_URL}/orders/edit"
GET_ONE_ORDER_ENDPOINT = f"{DISPATCHER_NODE_URL}/orders/get_one"