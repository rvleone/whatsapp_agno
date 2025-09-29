import os
import requests

WAHA_API_URL = os.getenv("WAHA_API_URL", "")
WAHA_SESSION_NAME = os.getenv("WAHA_SESSION_NAME", "")

def send_message(chat_id: str, message: str):

    headers = {
        "Content-Type": "application/json"
    }

    send_url = f"{WAHA_API_URL}/sendText"

    payload = {
        "session": WAHA_SESSION_NAME,
        "chatId": chat_id,
        "text": message
    }

    return requests.post(send_url, headers=headers, json=payload)
