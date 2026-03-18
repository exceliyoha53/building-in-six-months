import os
import requests
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = "1841231351"


def send_telegran_alert(message_text):
    """
    Delivers a text payload to a specific Telegram user via the official REST API.
    """
    api_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {"chat_id": CHAT_ID, "text": message_text}
    try:
        response = requests.post(url=api_url, json=payload)
        response.raise_for_status()
        print("Alert Successfully pushed to mobile device.")

    except requests.exceptions.RequestException as e:
        print(f"Critical failure delivering alert: {e}")


if __name__ == "__main__":
    text_message = "System Update: Master Engine comms link established. Awaiting orders."
    send_telegran_alert(text_message)
