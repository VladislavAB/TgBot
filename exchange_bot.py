import telebot
from Bot.config import TOKEN
from extensions import ConvertionException, CryptoConverter
import requests
import json

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start(message):
    text = (
        'Добрый день! Чтобы рассчитать стоимость валюты введите:'
        ' Имя валюты, цену которой Вы хотите узнать, имя валюты, в которой надо узнать цену первой валюты, '
        'количество переводимой валюты в следующем формате:\n'
        'BTC*пробел*RUB*пробел*15')
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def get_values(message):
    response = requests.get(
        'https://min-api.cryptocompare.com/data/blockchain/list'
        '?api_key=dd005136ec232f5307e63a9d803af76c34e309050954533014ee700dfc4d8f96')
    values = list(json.loads(response.text)['Data'].keys())
    total = 'Доступные валюты: '
    for token in values:
        total = '\n'.join((total, token))
    bot.send_message(message.chat.id, total)


@bot.message_handler()
def convert(message):
    try:
        values = message.text.split()
        if len(values) != 3:
            raise ConvertionException('Неверный формат ввода, повторите ввод!')
        quote, base, amount = values[0].upper(), values[1].upper(), values[2]
        total = CryptoConverter.get_price(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя. \n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду \n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} = {total}'
        bot.send_message(message.chat.id, text)


bot.infinity_polling()
