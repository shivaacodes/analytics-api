from typing import Union
from contextlib import asynccontextmanager
from api.db.session import init_db

from fastapi import FastAPI
from api.db.session import engine
from sqlmodel import SQLModel
from api.events import router as event_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🔥 Starting database initialization...")
    try:
        init_db()  # ✅ This includes hypertable creation!
        print("✅ Database and hypertable setup complete")
    except Exception as e:
        print(f"❌ Error during DB init: {e}")
        raise
    yield
    print("👋 Application shutdown...")

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
