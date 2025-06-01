from fastapi import APIRouter
from .schemas import EventSchema, EventListSchema

router = APIRouter()

@router.get("/", response_model=EventListSchema)
def read_events() -> EventListSchema:
    events = [EventSchema(id=i) for i in [1, 2, 3, 4, 5]]
    return EventListSchema(results=events, count=len(events))

@router.post("/", response_model=EventSchema)
def create_event(data:dict={}) -> EventSchema:
    print(data)
    return EventSchema(id=125)

@router.get("/{event_id}", response_model=EventSchema)
def get_event(event_id: int) -> EventSchema:
    return EventSchema(id=event_id)
