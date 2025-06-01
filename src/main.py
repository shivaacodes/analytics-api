from typing import Union

from fastapi import FastAPI
from api.events import router as event_router

app = FastAPI()
app.include_router(event_router, prefix='/api/events')

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def get_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

# Health check
@app.get("/healthz")
def read_api_health():
    return {"status": "ok"}
