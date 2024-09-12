import sqlite3
import dotenv
import os

dotenv.load_dotenv()
BAZA = os.getenv('BAZA')


def baza_write(request, parameters):
    global BAZA
    conn = sqlite3.connect(BAZA)
    cur = conn.cursor()
    cur.execute(request, parameters)
    conn.commit()
    cur.close()
    conn.close()


def baza_readall(request):
    global BAZA
    conn = sqlite3.connect(BAZA)
    cur = conn.cursor()
    cur.execute(request)
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data


def baza_readmy(request, parameters):
    global BAZA
    conn = sqlite3.connect(BAZA)
    cur = conn.cursor()
    cur.execute(request, parameters)
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data


def baza_delete(parameters, asker):
    global BAZA
    conn = sqlite3.connect(BAZA)
    cur = conn.cursor()
    cur.execute("select author from articles where id = ?", parameters)
    author = cur.fetchall()
    if len(author) == 1:
        if author[0][0] == asker:
            cur.execute("DELETE from articles where id = ?", parameters)
            conn.commit()
            answer = "Статья удалена"
        else:
            answer = 'Вы не можете удалить чужую статью'
    else:
        answer = 'В боте нет ни одной статьи'
    cur.close()
    conn.close()

    return answer