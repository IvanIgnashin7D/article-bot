from fastapi import *
from pydantic import BaseModel


app = FastAPI()


class Article(BaseModel):
    head: str
    text: str
    author: str


@app.post("/articles/add")
async def add_article(article: Article):
    import sqlite3
    import dotenv
    import os

    dotenv.load_dotenv()
    BAZA = os.getenv('BAZA')
    conn = sqlite3.connect(BAZA)
    cur = conn.cursor()
    print(BAZA)
    cur.execute('CREATE TABLE IF NOT EXISTS articles (id INTEGER PRIMARY KEY AUTOINCREMENT, head TEXT, txt TEXT, author TEXT)')
    conn.commit()
    cur.execute('INSERT INTO articles (head, txt, author) VALUES (?, ?, ?)', (article.head, article.text, article.author))
    conn.commit()
    cur.close()
    conn.close()

    return {'status': 'ok'}


@app.get('/articles/getall')
async def get_articles() -> list[Article]:
    import sqlite3
    import dotenv
    import os

    dotenv.load_dotenv()
    BAZA = os.getenv('BAZA')
    conn = sqlite3.connect(BAZA)
    cur = conn.cursor()
    cur.execute('SELECT * FROM articles')
    articles = cur.fetchall()
    cur.close()
    conn.close()

    return [Article(head=i[1], text=i[2], author=i[3]) for i in articles]
