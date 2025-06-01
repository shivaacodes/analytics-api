from typing import List
from pydantic import BaseModel

# Design of the database models
class EventSchema(BaseModel):
    id: int


class EventListSchema(BaseModel):
    results:List[EventSchema]
    count:int