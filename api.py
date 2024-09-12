from fastapi import *
from pydantic import BaseModel


app = FastAPI()


class Article(BaseModel):
    id: int = None
    head: str
    text: str
    author: str


class Author(BaseModel):
    name: str


class Article_to_delete(BaseModel):
    id: int
    asker: str


@app.post("/articles/add")
async def add_article(article: Article):
    import sqlite3
    import dotenv
    import os

    dotenv.load_dotenv()
    BAZA = os.getenv('BAZA')
    conn = sqlite3.connect(BAZA)
    cur = conn.cursor()
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

    return [Article(id=i[0], head=i[1], text=i[2], author=i[3]) for i in articles]


@app.get('/articles/my')
async def my_articles(author: str) -> list[Article]:
    import sqlite3
    import dotenv
    import os

    dotenv.load_dotenv()
    BAZA = os.getenv('BAZA')
    conn = sqlite3.connect(BAZA)
    cur = conn.cursor()
    cur.execute('SELECT * FROM articles WHERE author = ?', (author, ))
    articles = cur.fetchall()
    cur.close()
    conn.close()

    return [Article(id=i[0], head=i[1], text=i[2], author=i[3]) for i in articles]


@app.delete('/articles/delete')
async def delete_article(article: Article_to_delete):
    import sqlite3
    import dotenv
    import os

    dotenv.load_dotenv()
    BAZA = os.getenv('BAZA')
    conn = sqlite3.connect(BAZA)
    cur = conn.cursor()
    cur.execute("select author from articles where id = ?", (article.id, ))
    author = cur.fetchall()
    print(author)
    if author[0][0] == article.asker:
        cur.execute("DELETE from articles where id = ?", (article.id, ))
        conn.commit()
        answer = "Статья удалена"
    else:
        answer = 'Вы не можете удалить чужую статью'
    cur.close()
    conn.close()

    return answer

