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
    from baza_conn import baza_write
    baza_write(request='INSERT INTO articles (head, txt, author) VALUES (?, ?, ?)',
               parameters=(article.head, article.text, article.author))
    return {'status': 'ok'}


@app.get('/articles/getall')
async def get_articles() -> list[Article]:
    from baza_conn import baza_readall
    data = baza_readall(request='SELECT * FROM articles')
    return [Article(id=i[0], head=i[1], text=i[2], author=i[3]) for i in data]


@app.get('/articles/my')
async def my_articles(author: str) -> list[Article]:
    from baza_conn import baza_readmy
    data = baza_readmy(request='SELECT * FROM articles WHERE author = ?', parameters=(author, ))
    return [Article(id=i[0], head=i[1], text=i[2], author=i[3]) for i in data]


@app.delete('/articles/delete')
async def delete_article(article: Article_to_delete):
    from baza_conn import baza_delete
    data = baza_delete(parameters=(article.id, ),
                       asker=article.asker)
    return data

