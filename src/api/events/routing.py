from api.db.session import get_session
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlmodel import Session, select# orm

from typing import List
from .models import (
    EventModel,
    EventBucketSchema,
    EventCreateSchema,
    get_utc_now
)
from api.db.session import engine
from timescaledb.hyperfunctions import time_bucket
from sqlalchemy import case,func

router = APIRouter()

DEFAULT_LOOKUP_PAGES = [
     "/", "/about", "/pricing", "/contact", 
        "/blog", "/products", "/login", "/signup",
        "/dashboard", "/settings"
    ]

#Get All Evnets: GET method
@router.get("/", response_model=List[EventBucketSchema])
def read_events(
    duration: str = Query(default="2 hours"),
    pages: List[str] = Query(default=None),
    session: Session = Depends(get_session)
):
    from sqlalchemy import String
    os_case = case(
        (func.lower(EventModel.user_agent).like('%windows%'), 'Windows'),
        (func.lower(EventModel.user_agent).like('%macintosh%'), 'MacOS'),
        (func.lower(EventModel.user_agent).like('%iphone%'), 'iOS'),
        (func.lower(EventModel.user_agent).like('%android%'), 'Android'),
        (func.lower(EventModel.user_agent).like('%linux%'), 'Linux'),
        else_='Other'
    ).label('operating_system')
    
    bucket = time_bucket("1 minute", EventModel.time)
    lookup_pages = pages if isinstance(pages, list) and len(pages) > 0 else DEFAULT_LOOKUP_PAGES

    query = (
        select(
            bucket.label('bucket'),
            os_case,
            EventModel.page.label('page'), # type: ignore
            func.count().label('count')
        )
        .where(
            EventModel.page.in_(lookup_pages)  # type: ignore
        )
        .group_by(*[col for col in [bucket,os_case, EventModel.page] if col is not None])
        
        .order_by(*[col for col in [bucket,os_case, EventModel.page] if col is not None])
    )
    results = session.exec(query).fetchall()
    return results


#Get a specific event GET /api/events/8
@router.get("/{event_id}", response_model=EventModel)
def get_event(event_id: int, session: Session = Depends(get_session)):
    query = select(EventModel).where(EventModel.id == event_id)
    result = session.exec(query).first()
    if not result:
        raise HTTPException(status_code=404, detail="Event not found")
    return result


#Create a New Event : POST /api/events
@router.post("/", response_model=EventModel)
def create_event(payload: EventCreateSchema, session: Session = Depends(get_session)):
    # print(type(payload.page)) payload->dict->pydantic
    data=payload.model_dump()
    obj=EventModel.model_validate(data)

    session.add(obj)
    session.commit()  # actually adding to the db
    session.refresh(obj)
    return obj