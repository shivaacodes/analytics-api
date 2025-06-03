from typing import Union
from contextlib import asynccontextmanager
import time

from fastapi import FastAPI
from api.db.session import init_db, engine
from sqlmodel import SQLModel
from api.events import router as event_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # before app startup
    print("Starting database initialization...")
    try:
        # Create all tables
        SQLModel.metadata.create_all(engine)
        print("Database tables created successfully")
    except Exception as e:
        print(f"Error creating database tables: {str(e)}")
        raise
    yield
    # cleanup

app = FastAPI(lifespan=lifespan)
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
