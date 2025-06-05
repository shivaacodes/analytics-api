import sqlmodel
from sqlmodel import SQLModel, Session
import time
from sqlalchemy import text
from .config import DATABASE_URL

if not isinstance(DATABASE_URL, str) or DATABASE_URL.strip() == "":
    raise NotImplementedError("DATABASE URL needs to be set!")

engine = sqlmodel.create_engine(DATABASE_URL, echo=True)  # Enable echo for SQL visibility

def init_db():
    max_retries = 5
    retry_delay = 5  # seconds

    for attempt in range(max_retries):
        try:
            print(f"🔄 Attempting to create database tables (attempt {attempt + 1}/{max_retries})")
            SQLModel.metadata.create_all(engine)
            print("✅ Database tables created successfully")

            with engine.connect() as conn:
                print("🧪 Checking TimescaleDB extension...")
                conn.execute(text("CREATE EXTENSION IF NOT EXISTS timescaledb;"))

                # Check if table exists
                result = conn.execute(
                    text("SELECT to_regclass('public.eventmodel');")
                ).scalar()
                if result is None:
                    raise Exception("❌ Table 'eventmodel' does not exist in database!")

                print("🧩 Creating hypertable for 'eventmodel' on column 'updated_at'...")
                result = conn.execute(
                    text("""
                        SELECT create_hypertable('eventmodel', 'updated_at', if_not_exists => TRUE);
                    """)
                )
                conn.commit()
                print("✅ Hypertable creation attempted successfully.")
                return

        except Exception as e:
            print(f"⚠️ Error during DB init: {e}")
            if attempt < max_retries - 1:
                print(f"⏳ Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                print("❌ Failed to initialize DB after all retries.")
                raise

def get_session():
    with Session(engine) as session:
        yield session
