from fastapi import *
from pydantic import BaseModel


app = FastAPI()


class New(BaseModel):
    name: str
    age: int


@app.post("/hello/")
async def add(res: New):
    return {"message": res.name}