import telebot
import requests
import json

TOKEN = '6906216735:AAEGcN4DdRXahAKp8FWnWiTCvcVHqE2anJM' 

bot = telebot.TeleBot(TOKEN)

keys = {
    'евро': 'EUR',
    'доллар': 'USD',
    'рубль': 'RUB',
}

class ConvertionException(Exception):
    pass

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу, введите команду в формате:\n <валюта> <в какую валюту перевести> <сумма>\n' \
           'Список всех доступных валют /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text += '\n' + key
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        currency_values = message.text.split(' ')
        
        if len(currency_values) != 3:
            raise ConvertionException('Неверное количество параметров.')

        quote, base, amount = currency_values

        if quote not in keys:
            raise ConvertionException(f'Валюта {quote} не найдена.')
        if base not in keys:
            raise ConvertionException(f'Валюта {base} не найдена.')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Неверное значение суммы: {amount}.')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={keys[quote]}&tsyms={keys[base]}')

        if r.status_code != 200:
            raise ConvertionException(f'Не удалось получить данные. Статус код: {r.status_code}')

        total_base = json.loads(r.content)[keys[base]]
        total_amount = total_base * amount
        text = f'Цена {amount} {quote} в {base} - {total_amount} {base}'
        
        bot.send_message(message.chat.id, text)

    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка конвертации: \n{e}')
    except Exception as e:
        bot.reply_to(message, f'Произошла непредвиденная ошибка:\n{e}')

bot.polling()