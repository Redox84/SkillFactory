import requests
import json
from config import keys

class ConvertionException(Exception):
    pass

class CriptoConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f'Я валюту {quote} не знаю')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f'Я валюту {base} не знаю')

        if quote == base:
            raise ConvertionException('Невозможно перевести одинаковые валюты')

        try:
            amount = float(amount.replace(",", "."))
        except ValueError:
            raise ConvertionException(f'Не верно введено количество валюты: {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]] * amount
        return total_base