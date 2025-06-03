from api.db.session import get_session
from fastapi import APIRouter,HTTPException,Depends
from sqlmodel import Session,select #orm

from .models import (
    EventModel, 
    EventListSchema, 
    EventCreateSchema,
    EventUpdateSchema
)

router = APIRouter()

#Get All Evnets: GET method
@router.get("/", response_model=EventListSchema)
def read_events(session:Session=Depends(get_session)):
    query=select(EventModel)
    results = list(session.exec(query).all())
    return EventListSchema(results=results, count=len(results))

#Get a specific event GET /api/events/8
@router.get("/{event_id}",response_model=EventModel)
def get_event(event_id:int,session:Session=Depends(get_session)):
    event=session.get(EventModel,event_id)
    if not event:
        raise HTTPException(status_code=404,detail="Event not found")
    return event
    

#Create a New Event : POST /api/events
@router.post("/", response_model=EventModel)
#Efficient way of adding a data to teh database
def create_event(payload:EventCreateSchema,session: Session=Depends(get_session)):
    # print(type(payload.page)) payload->dict->pydantic
    obj=EventModel.model_validate(payload) #instance of that model OR row of that class

    session.add(obj)
    session.commit()# actually adding to the db
    session.refresh(obj)
    return obj

# Update this id :/api/events/12
@router.put("/{event_id}",response_model=EventModel)
def update_event(event_id:int, payload:EventUpdateSchema,session:Session=Depends(get_session)):
    event=session.get(EventModel,event_id)

    if not event:
        raise HTTPException(status_code=404,detail="Event not found")
    
    for key,value in payload.model_dump(exclude_unset=True).items():
        setattr(event,key,value)

    session.add(event)
    session.commit()
    session.refresh(event)
    return event