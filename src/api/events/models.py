from datetime import datetime
from typing import List, Optional
from sqlmodel import SQLModel,Field
from timescaledb import TimescaleModel
from timescaledb.utils import get_utc_now
from sqlalchemy import Text, Column, Integer

# def get_utc_now():
#     return datetime.now(timezone.utc).replace(tzinfo=timezone.utc)

#page visits at any given time

#Database itself
class EventModel(TimescaleModel,table=True):
    page:str=Field(index=True) # /about, /pricing , /contact page etc
    user_agent:Optional[str]=Field(default="",index=True) #browser
    ip_address:Optional[str]=Field(default="",index=True)
    referrer:Optional[str]=Field(default="",index=True)
    session_id:Optional[str]=Field(index=True)
    duration:Optional[int]=Field(default=0, sa_column=Column(Integer))
    
    __chunk_time_interval__="INTERVAL 1 day"
    __drop_after__="INTERVAL 1 month"
    
    # id: Optional[int] = Field(
    #     default=None,
    #     primary_key=True
    # )
    updated_at:datetime =Field(
        default_factory=get_utc_now,
        primary_key=True
        )
    #time: datetime = Field(default_factory=get_utc_now)
   
    #description:Optional[str] = Field(default=None, sa_column=Column(Text))

    # created_at:datetime =Field(
    #     default_factory=get_utc_now,
    #     nullable=False
    #     )
    
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
    user_agent:Optional[str]=Field(default="",index=True)
    ip_address:Optional[str]=Field(default="",index=True)
    referrer:Optional[str]=Field(default="",index=True)
    session_id:Optional[str]=Field(index=True)
    duration:Optional[int]=Field(default=0)
    
class EventBucketSchema(SQLModel):
    bucket:datetime
    page:str
    ua:Optional[str]=""
    operating_system:Optional[str]=""
    duration: Optional[str] = Field(default=0)
    count:int