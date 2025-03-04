from dotenv import load_dotenv
from telebot import TeleBot, types
import os
import requests


load_dotenv()
secret_token = os.getenv('TOKEN')
bot = TeleBot(token=secret_token)
URL = 'https://api.thecatapi.com/v1/images/search'


def get_image():
    response = requests.get(URL).json()
    random_cat = response[0].get('url')
    return random_cat


@bot.message_handler(commands=['newcat'])
def new_cat(message):
    chat = message.chat
    bot.send_photo(chat.id, get_image())


@bot.message_handler(commands=['start'])
def wake_up(message):
    chat = message.chat
    name = chat.first_name
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(
        types.KeyboardButton('Который час?'),
        types.KeyboardButton('Определи мой ip'),
    )
    keyboard.row(
        types.KeyboardButton('/random_digit')
    )
    button_newcat = types.KeyboardButton('/newcat')
    keyboard.add(button_newcat)
    bot.send_message(
        chat_id=chat.id,
        text=f'Привет, {name}. Посмотри, какого котика я тебе нашёл',
        reply_markup=keyboard,
        )
    bot.send_photo(chat.id, get_image())


@bot.message_handler(content_types=['text'])
def say_hi(message):
    chat = message.chat
    chat_id = chat.id
    bot.send_message(chat_id=chat_id, text='Привет, я KittyBot!')


bot.polling()
