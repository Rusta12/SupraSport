import requests
import json

from config import catalog_ya, ya_api
from get_db_structure import get_db_structure_with_data

#database_structure = get_db_structure_with_data()


def ya_gpt(message):
    prompt = {
        "modelUri": catalog_ya,
        "completionOptions": {
            "stream": False,
            "temperature": 0.1,
            "maxTokens": "2000"
        },
        "messages": [
            {
                "role": "system",
                "text": f"Бот SupraSport помошник для корректного формулирования фраз для официальных писем по спортивной направленности"
            },
            {
                "role": "user",
                "text": f"{message}"
            }
        ]
    }

    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-Key {ya_api}"
    }
    try:
        response = requests.post(url, headers=headers, json=prompt)
        response.raise_for_status()  # Проверка на ошибки HTTP
        data = response.json()
        # Логируем весь ответ для отладки
        #print("Ответ от API:", json.dumps(data, indent=4))
        # Извлечение текста из ответа
        text = data["result"]["alternatives"][0]["message"]["text"]
        return text
    except Exception as e:
        print(f"Ошибка: {e}")

