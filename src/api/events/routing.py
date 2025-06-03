from api.db.session import get_session
from fastapi import APIRouter,HTTPException,Depends
from sqlmodel import Session,select,desc#orm
from .models import (
    EventModel, 
    EventListSchema, 
    EventCreateSchema,
    EventUpdateSchema,
    get_utc_now
)

router = APIRouter()

#Get All Evnets: GET method
@router.get("/", response_model=EventListSchema)
def read_events(session:Session=Depends(get_session)):
    query=select(EventModel).order_by(desc(EventModel.id)).limit(95)
    results = list(session.exec(query).all())
    return EventListSchema(results=results, count=len(results))

#Get a specific event GET /api/events/8
@router.get("/{event_id}",response_model=EventModel)
def get_event(event_id:int,session:Session=Depends(get_session)):
    query=select(EventModel).where(EventModel.id==event_id)
    result=session.exec(query).first()
    if not result:
        raise HTTPException(status_code=404,detail="Event not found")
    return result
    

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
    query=select(EventModel).where(EventModel.id==event_id)
    obj=session.exec(query).first()
    if not obj:
        raise HTTPException(status_code=404,detail="Event not found")
    
    for key,value in payload.model_dump(exclude_unset=True).items():
        setattr(obj,key,value)
    
    obj.updated_at=get_utc_now()
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj