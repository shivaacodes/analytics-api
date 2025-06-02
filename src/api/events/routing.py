import os
from fastapi import APIRouter
from .models import (
    EventModel, 
    EventListSchema, 
    EventCreateSchema,
    EventUpdateSchema
)

router = APIRouter()
from ..db.config import DATABASE_URL

#Get aLL Evnets
@router.get("/", response_model=EventListSchema)
def read_events() -> EventListSchema:
    events = [EventModel(id=i) for i in [1, 2, 3, 4, 5]]
    print(os.environ.get("DATABASE_URL"),DATABASE_URL) # Both works in my system 
    return EventListSchema(results=events, count=len(events))

#Get a specific event
@router.get("/{event_id}", response_model=EventModel)
def get_event(event_id: int) -> EventModel:
    return EventModel(id=event_id)

#Create a New Event
@router.post("/", response_model=EventModel)
def create_event(payload:EventCreateSchema) -> EventModel:
    print(type(payload.page))
    return EventModel(id=125,page=payload.page)

# Update this id :/api/events/12
@router.put("/{event_id}")
def update_event(event_id:int, payload:EventUpdateSchema)->EventModel:
    print(payload.description)
    return EventModel(id=event_id,description=payload.description)