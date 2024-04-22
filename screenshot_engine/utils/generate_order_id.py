import uuid

def generate_order_id() -> str:
    return str(uuid.uuid4())


print(generate_order_id(    ))

