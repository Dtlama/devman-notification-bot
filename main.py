import os
from time import sleep
import requests
import telegram
from dotenv import load_dotenv


if __name__ == '__main__':
    load_dotenv()

    devman_token = os.environ['DEVMAN_TOKEN']
    tg_token = os.environ['TG_TOKEN']
    tg_chat_id = os.environ['TG_CHAT_ID']

    timestamp = None

    headers = {
        'Authorization': devman_token
    }

    url = "https://dvmn.org/api/long_polling/"

    bot = telegram.Bot(token=tg_token)

    while True:
        message = """У вас проверили работу{lesson_title}
        {status}
        Ссылка на работу{lesson_url}"""
        try:
            payload = {"timestamp": timestamp}
            response = requests.get(url, headers=headers, params=payload)
            response.raise_for_status()
            response_payload = response.json()
            timestamp = response_payload.get("last_attempt_timestamp")
            if not timestamp:
                timestamp = response_payload.get("timestamp_to_request")

            if response_payload.get("status") == "found":
                lesson_title = response_payload["new_attempts"][0]["lesson_title"]
                lesson_url = response_payload["new_attempts"][0]["lesson_url"]
                if response_payload.get("is_negative"):
                    status = "Преподавателю всё понравилось, можно приступать к следующему уроку!"
                else:
                    status = "К сожалению, в работе нашлись ошибки."
                message = message.format(lesson_title=lesson_title, status=status, lesson_url=lesson_url)
        except requests.exceptions.ReadTimeout:
            pass
        except requests.exceptions.ConnectionError:
            print('ConnectionError')
            sleep(5)
