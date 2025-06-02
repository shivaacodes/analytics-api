import sqlmodel
from sqlmodel import SQLModel
from .config import DATABASE_URL

if not isinstance(DATABASE_URL, str) or DATABASE_URL.strip() == "":
    raise NotImplementedError("DATABASE URL needs to be set!")

engine = sqlmodel.create_engine(DATABASE_URL)

def init_db():
    print("creating database")
    SQLModel.metadata.create_all(engine) # connect to the model(database)