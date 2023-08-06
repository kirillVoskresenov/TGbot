import requests
import json

class APIException(Exception):
    pass

class Convertor:
    @staticmethod
    def get_price(base,quote,amount):
        if quote == base:
            raise APIException(f"Невозможно перевести одинаковые валюты {base}!")

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}!')


        url = f'https://api.apilayer.com/exchangerates_data/convert?to={quote}&from={base}&amount={amount}'

        headers = {
            "apikey": "SMAkixRnu3AZxbSfp7KTRq8moivxdGZj"
        }

        response = requests.get(url, headers=headers)
        result = response.json()
        converted_amount = result['result']

        return converted_amount
