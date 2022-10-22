import os
import requests
import telegram

devman_token = os.environ['TOKEN']
tg_token = os.environ['TG_TOKEN']
tg_chat_id = os.environ['CHAT_ID']

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
        timestamp = response.json().get("last_attempt_timestamp")
        if not timestamp:
            timestamp = response.json().get("timestamp_to_request")
        print(response.json())

        if response.json().get("status") == "found":
            lesson_title = response.json()["new_attempts"][0]["lesson_title"]
            lesson_url = response.json()["new_attempts"][0]["lesson_url"]
            if response.json().get("is_negative"):
                status = "Преподавателю всё понравилось, можно приступать к следующему уроку!"
            else:
                status = "К сожалению, в работе нашлись ошибки."
            message = message.format(lesson_title=lesson_title, status=status, lesson_url=lesson_url)
    except requests.exceptions.ReadTimeout:
        print('ReadTimeout')
    except requests.exceptions.ConnectionError:
        print('ConnectionError')
