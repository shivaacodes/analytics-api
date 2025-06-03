import sqlmodel
from sqlmodel import SQLModel, Session
from .config import DATABASE_URL
import time

if not isinstance(DATABASE_URL, str) or DATABASE_URL.strip() == "":
    raise NotImplementedError("DATABASE URL needs to be set!")

engine = sqlmodel.create_engine(DATABASE_URL)

def init_db():
    max_retries = 5
    retry_delay = 5  # seconds
    
    for attempt in range(max_retries):
        try:
            print(f"Attempting to create database tables (attempt {attempt + 1}/{max_retries})")
            SQLModel.metadata.create_all(engine)
            print("Database tables created successfully")
            return
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"Failed to create database tables: {str(e)}")
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                print("Failed to create database tables after all retries")
                raise

def get_session():
    with Session(engine) as session:
        yield session