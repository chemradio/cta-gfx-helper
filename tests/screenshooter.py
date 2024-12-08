import requests

# The URL of your FastAPI endpoint
url = "http://127.0.0.1:9002/"  # Change this to your actual FastAPI server URL


def add_order():
    # The other form data (optional)
    data = {"screenshot_link": ""}

    # Make the POST request
    response = requests.post(
        url,
        data=data,
        # json=data,
    )

    # Print the response
    print(response.status_code)
    print(response.text)


def check_order(order_id: str):
    data = {"order_id": order_id}
    response = requests.get(url, json=data)

    return response.json()


# add_order()
# print(check_order(""))
