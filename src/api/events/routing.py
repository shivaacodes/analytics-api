from fastapi import APIRouter
from .schemas import (
    EventSchema, 
    EventListSchema, 
    EventCreateSchema,
    EventUpdateSchema
)

router = APIRouter()

#Get aLL Evnets
@router.get("/", response_model=EventListSchema)
def read_events() -> EventListSchema:
    events = [EventSchema(id=i) for i in [1, 2, 3, 4, 5]]
    return EventListSchema(results=events, count=len(events))

#Get a specific event
@router.get("/{event_id}", response_model=EventSchema)
def get_event(event_id: int) -> EventSchema:
    return EventSchema(id=event_id)

#Create a New Event
@router.post("/", response_model=EventSchema)
def create_event(payload:EventCreateSchema) -> EventSchema:
    print(type(payload.page))
    return EventSchema(id=125,page=payload.page)

# Update this id :/api/events/12
@router.put("/{event_id}")
def update_event(event_id:int, payload:EventUpdateSchema)->EventSchema:
    print(payload.description)
    return EventSchema(id=event_id,description=payload.description)