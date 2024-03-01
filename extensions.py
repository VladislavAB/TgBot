import requests
import json


class ConvertionException(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def get_price(quote, base, amount):
        if quote == base:
            raise ConvertionException('Невозможно перевести одинаковые валюты!')
        try:
            amount == float(amount)
        except ValueError:
            raise ConvertionException('Третьим параметром должно быть число')
        response = requests.get(
            f'https://min-api.cryptocompare.com/data/price?fsym={quote}&tsyms={base}')
        total = round(json.loads(response.content)[base.upper()] * float(amount), 8)
        return total
