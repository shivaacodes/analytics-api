from datetime import datetime
from typing import List, Optional
from sqlmodel import SQLModel,Field
from timescaledb import TimescaleModel
from timescaledb.utils import get_utc_now
from sqlalchemy import Text, Column

# def get_utc_now():
#     return datetime.now(timezone.utc).replace(tzinfo=timezone.utc)

#page visits at any given time

#Database itself
class EventModel(TimescaleModel,table=True):
    # id: Optional[int] = Field(
    #     default=None,
    #     primary_key=True
    # )
    updated_at:datetime =Field(
        default_factory=get_utc_now,
        primary_key=True
        )
    time: datetime = Field(default_factory=get_utc_now)
    page:str=Field(index=True) # /about, /pricing , /contact page etc
    description:Optional[str] = Field(default=None, sa_column=Column(Text))

    # created_at:datetime =Field(
    #     default_factory=get_utc_now,
    #     nullable=False
    #     )
    
    __chunk_time_interval__="INTERVAL 1 day"
    __drop_after__="INTERVAL 1 month"
'''
note:TimescaleDB splits data into chunks based on time (updated_at), 
but those chunks must have unique rows. If you're using a primary key on the table, then 
Timescale requires the partitioning column (updated_at) to be part of the 
primary key, or else it cannot guarantee row uniqueness across time partitions.
'''
class EventListSchema(SQLModel):
    results:List[EventModel]
    count:int

class EventCreateSchema(SQLModel):
    page:str
    description:Optional[str]=Field(default="")

class EventUpdateSchema(SQLModel):
    description:str