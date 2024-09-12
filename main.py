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


article = {}

button1 = types.KeyboardButton(text='Создать статью')
button2 = types.KeyboardButton(text='Просмотреть все статьи')
button3 = types.KeyboardButton(text='Просмотреть мои статьи')
welcome_keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=2, resize_keyboard=True, ).add(button1, button2, button3)


@bot.message_handler(commands=['start'])
def start(message):
    global welcome_keyboard
    bot.send_message(message.chat.id, text='Это бот для создания статей.', reply_markup=welcome_keyboard)


@bot.message_handler(commands=['newarticle'])
@bot.message_handler(func=lambda message: message.text in ['i', 'Создать статью'])
def api(message):
    sent = bot.send_message(message.chat.id, text='Введите заголовок статьи')
    bot.register_next_step_handler(sent, article_text)


def article_text(message):
    article['head'] = message.text
    sent = bot.send_message(message.chat.id, text='Введите текст статьи')
    bot.register_next_step_handler(sent, article_commit)


def article_commit(message):
    global welcome_keyboard
    article['text'] = message.text
    article['author'] = message.from_user.first_name
    response = requests.post('http://127.0.0.1:8000/articles/add', json=article)
    if response.status_code == 200:
        bot.send_message(message.chat.id, text='Статья создана', reply_markup=welcome_keyboard)
    else:
        bot.send_message(message.chat.id, text=f'Ошибка при добавлении статьи: {response.status_code} {response.text}', reply_markup=welcome_keyboard)
        print("Ошибка при добавлении статьи:", response.status_code, response.text)


@bot.message_handler(commands=['allarticles'])
@bot.message_handler(func=lambda message: message.text in ['a', 'Просмотреть все статьи'])
def get_articles(message):
    global welcome_keyboard
    response = requests.get('http://127.0.0.1:8000/articles/getall')
    if response.status_code == 200:
        response = response.json()
        for i in response:
            bot.send_message(message.chat.id, text=f'Статья {i["id"]}\n{i["head"]} \n\n{i["text"]} \n\nАвтор: {i["author"]}')
        bot.send_message(message.chat.id, text='Выберите действие', reply_markup=welcome_keyboard)
    else:
        bot.send_message(message.chat.id, text='Ошибка при получении данных.', reply_markup=welcome_keyboard)
        print('Ошибка при получении данных.', response.status_code, response.text)


@bot.message_handler(func=lambda message: message.text in ['Просмотреть мои статьи'])
def my_articles(message):
    global welcome_keyboard
    response = requests.get('http://127.0.0.1:8000/articles/my', params={'author': message.from_user.first_name})
    if response.status_code == 200:
        response = response.json()
        for i in response:
            bot.send_message(message.chat.id, text=f'Статья {i["id"]}\n{i["head"]} \n\n{i["text"]} \n\nАвтор: {i["author"]}', reply_markup=welcome_keyboard)


@bot.message_handler(func=lambda message: message.text in ['d'])
def delete_article(message):
    my_articles(message)
    sent = bot.send_message(message.chat.id, text='Введите номер статьи, которую хотите удалить:')
    bot.register_next_step_handler(sent, delete_article2)


def delete_article2(message):
    global welcome_keyboard
    id = message.text
    params = {"id": id, 'asker': message.from_user.first_name}
    response = requests.delete(url='http://127.0.0.1:8000/articles/delete', json=params)
    if response.status_code == 200:
        txt = response.text
        bot.send_message(message.chat.id, text=txt, reply_markup=welcome_keyboard)


bot.polling()
