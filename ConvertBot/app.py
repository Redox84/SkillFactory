import telebot
from config import *
from extensions import ConvertionException, CriptoConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    text = 'Приветствую Вас, я умею конвертировать валюты.\n'\
           'Для получение подробной информации нажмите /help'
    bot.reply_to(message, text)

@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    text = 'Увидеть список всех доступных валют: /values.\n'\
           'Чтобы начать конвертировать введите команду боту /convert'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступны валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)

@bot.message_handler(commands=['convert'])
def start(message: telebot.types.Message):
    text = 'Выберете валюту, из которой конвертировать:'
    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, base_handler)

def base_handler(message: telebot.types.Message):
    base = message.text.strip()
    text = 'Выберете валюту, в которую конвертировать:'
    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, quote_handler, base)

def quote_handler(message: telebot.types.Message, base):
    quote = message.text.strip()
    text = 'Выберете количество валюты:'
    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, amount_handler, base, quote)

def amount_handler(message: telebot.types.Message, base, quote):
    amount = message.text.strip()
    try:
        total_base = CriptoConverter.get_price(quote, base, amount)

    except ConvertionException as e:
        bot.send_message(message.chat.id, f'Ошибка ввода данных\n{e}')
    except Exception as e:
        bot.send_message(message.chat.id, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base}: {total_base}'
    bot.send_message(message.chat.id, text)

bot.polling()