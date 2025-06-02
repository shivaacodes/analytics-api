from typing import List, Optional
from pydantic import BaseModel, Field

"""
id
path
description
"""

# Design of the database models
class EventSchema(BaseModel):
    id: int
    page:Optional[str]=""
    description:Optional[str]=Field(default="My description")


class EventListSchema(BaseModel):
    results:List[EventSchema]
    count:int

class EventCreateSchema(BaseModel):
    page:str

class EventUpdateSchema(BaseModel):
    description:str