import requests
import json
from Config import keys


class ConvertionException(Exception):
    pass


class CriptoConverter:
    @staticmethod
    def convert(fsym: str, tsyms: str, sym: str):
        if fsym == tsyms:
            raise ConvertionException(f"Невозможно перевести одно значение: {fsym}, /help")

        try:
            fsym_ticet = keys[fsym]
        except KeyError:
            raise ConvertionException(f"Валюта {fsym} не найдена, /values")

        try:
            tsyms_ticet = keys[tsyms]
        except KeyError:
            raise ConvertionException(f"Валюта {tsyms} не найдена, /values")

        try:
            sym = float(sym)
        except ValueError:
            raise ConvertionException(f"Не удалось обработать кол-во валюты{sym}, /help")

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={fsym_ticet}&tsyms={tsyms_ticet}')
        total = (json.loads(r.content)[tsyms_ticet])
        total = total * sym
        return f"{total:.2f}"

