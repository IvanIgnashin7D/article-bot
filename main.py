from telebot import *
import sqlite3
import dotenv
import os
from api import add


dotenv.load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
bot = TeleBot(token=TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, text='Старт')


@bot.message_handler(func=lambda message: message.text in ['i', 'Создать статью'])
def api(message):
    add()



bot.polling()