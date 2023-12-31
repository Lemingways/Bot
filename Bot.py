import telebot
from Config import keys, TOKEN, cats
from utils_bot import CriptoConverter, ConvertionException
from telebot import types


bot = telebot.TeleBot(TOKEN)
cats_counter = 0


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item_helper = types.KeyboardButton("Как использовать бота?🔍")
    item_values = types.KeyboardButton("Какие валюты доступны?🏦")
    item_cats = types.KeyboardButton("Фото котика")
    markup.add(item_helper, item_values, item_cats)

    bot.send_message(message.chat.id, "Привет!!!\nЧто бы начать работу введите команду в след формате:\n<Имя валюты> \
 <В какую валюту перевести> \
 <кол-во переводимой валюты> \
 \n \
\nПример: Биткоин Доллар 2".format(message.from_user), reply_markup=markup)


@bot.message_handler(content_types=['text'])
def cat(massage: telebot.types.Message):
    global cats_counter
    text = " Извините к сожелению котики кончились 😭😢💔\n\
Но вы можете посмотреть на них eщё раз 😊😊😊"
    pic = cats[cats_counter]
    if cats_counter == len(cats) - 1:
        bot.send_message(massage.chat.id, text)
        cats_counter = -1
    if massage.chat.type == 'private':
        if "Фото котика" in massage.text:
            bot.send_photo(massage.chat.id, pic)
            cats_counter += 1
        else:
            values(massage)


@bot.message_handler(content_types=['text'])
def values(message: telebot.types.Message):
    text = "Доступные валюты:"
    if message.chat.type == 'private':
        if "Какие валюты доступны?" in message.text or message.text == "/values":
            for key in keys.keys():
                text = '\n'.join((text, key))
            bot.reply_to(message, text)
        else:
            helper(message)


@bot.message_handler(content_types=['text'])
def helper(message: telebot.types.Message):
    text = "Что бы начать работу введите команду в след формате:\n<Имя валюты> \
 <В какую валюту перевести> \
 <кол-во переводимой валюты> \
 \n \
 \nПример: Биткоин Доллар 2"
    if message.chat.type == 'private':
        if "Как использовать бота?" in message.text or message.text == "/help":
            bot.reply_to(message, text)
        else:
            convert(message)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:

        values = message.text.split(" ")

        if len(values) < 3:
            raise ConvertionException("Недостаточно параметров, /help")

        if len(values) > 3:
            raise ConvertionException("Слишком много параметров, /help")

        fsym, tsyms, sym = values
        total = CriptoConverter.convert(fsym, tsyms, sym)
    except ConvertionException as e:
        bot.reply_to(message, f"Ошибка пользователя\n{e}")
    except Exception as e:
        bot.reply_to(message, f"Не удалось обработать команду\n{e}")
    else:
        text = f"Цена {sym} {keys[fsym]} в {keys[tsyms]}: {total}"
        bot.send_message(message.chat.id, text)


bot.polling()
