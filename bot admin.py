from telebot import *
import sqlite3
import dotenv
import os
import requests


dotenv.load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
bot = TeleBot(token=TOKEN)


BAZA = os.getenv('BAZA')
conn = sqlite3.connect(BAZA)
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS articles (id INTEGER PRIMARY KEY AUTOINCREMENT, head TEXT, txt TEXT, author TEXT)')
conn.commit()
cur.close()
conn.close()