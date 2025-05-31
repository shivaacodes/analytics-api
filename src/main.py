from fastapi import FastAPI
from typing import Union

app=FastAPI()

@app.get("/")
def first_api():
    return {"Hello":"world"}

@app.get("/items/{item_id}")
def get_item(item_id: int,q: Union[str, None]=None):
    return{"item_id":item_id,"q":q}