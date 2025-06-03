from datetime import datetime, timezone
from typing import List, Optional
from sqlmodel import SQLModel,Field

def get_utc_now():
    return datetime.now(timezone.utc).replace(tzinfo=timezone.utc)

#Database itself
class EventModel(SQLModel,table=True):
    id: Optional[int]=Field(default=None,primary_key=True)
    page:Optional[str]=Field(default=None)
    description:Optional[str]=Field(default=None)
    created_at:datetime =Field(
        default_factory=get_utc_now,
        nullable=False
        )
    updated_at:datetime =Field(
        default_factory=get_utc_now,
        nullable=False
        )

class EventListSchema(SQLModel):
    results:List[EventModel]
    count:int

class EventCreateSchema(SQLModel):
    page:str
    description:Optional[str]=Field(default="")

class EventUpdateSchema(SQLModel):
    description:str