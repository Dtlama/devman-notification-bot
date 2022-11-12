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
            review_info = response.json()
            timestamp = review_info.get("last_attempt_timestamp")
            if not timestamp:
                timestamp = review_info.get("timestamp_to_request")

            if review_info.get("status") == "found":
                lesson_title = review_info["new_attempts"][0]["lesson_title"]
                lesson_url = review_info["new_attempts"][0]["lesson_url"]
                if review_info.get("is_negative"):
                    status = "Преподавателю всё понравилось, можно приступать к следующему уроку!"
                else:
                    status = "К сожалению, в работе нашлись ошибки."
                message = message.format(lesson_title=lesson_title, status=status, lesson_url=lesson_url)
        except requests.exceptions.ReadTimeout:
            pass
        except requests.exceptions.ConnectionError:
            print('ConnectionError')
            sleep(5)
