from sqlalchemy.orm import Session
from . import models, schemas

def create_region(db: Session, region: schemas.RegionCreate):
    db_region = models.Region(**region.model_dump())
    db.add(db_region)
    db.commit()
    db.refresh(db_region)
    return db_region

def get_region(db: Session, region_id: int):
    return db.query(models.Region).filter(models.Region.id == region_id).first()

def create_hotel(db: Session, hotel: schemas.HotelCreate):
    db_hotel = models.Hotel(**hotel.model_dump())
    db.add(db_hotel)
    db.commit()
    db.refresh(db_hotel)
    return db_hotel

def get_hotel(db: Session, hotel_id: int):
    return db.query(models.Hotel).filter(models.Hotel.id == hotel_id).first()

def create_activity(db: Session, activity: schemas.ActivityCreate):
    db_activity = models.Activity(**activity.model_dump())
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    return db_activity

def create_transfer(db: Session, transfer: schemas.TransferCreate):
    db_transfer = models.Transfer(**transfer.model_dump())
    db.add(db_transfer)
    db.commit()
    db.refresh(db_transfer)
    return db_transfer

def create_day(db: Session, day: schemas.DayCreate):
    db_day = models.Day(day_number=day.day_number, hotel_id=day.hotel_id)
    db.add(db_day)
    db.commit()
    db.refresh(db_day)
    
    for activity in day.activities:
        activity_data = activity.model_dump()
        activity_data["day_id"] = db_day.id
        create_activity(db, schemas.ActivityCreate(**activity_data))
    
    for transfer in day.transfers:
        transfer_data = transfer.model_dump()
        transfer_data["day_id"] = db_day.id
        create_transfer(db, schemas.TransferCreate(**transfer_data))
    
    return db_day

def create_itinerary(db: Session, itinerary: schemas.ItineraryCreate):
    db_itinerary = models.Itinerary(
        title=itinerary.title,
        duration_nights=itinerary.duration_nights,
        region_id=itinerary.region_id
    )
    db.add(db_itinerary)
    db.commit()
    db.refresh(db_itinerary)
    
    for day in itinerary.days:
        day_data = day.model_dump()
        day_data["itinerary_id"] = db_itinerary.id
        create_day(db, schemas.DayCreate(**day_data))
    
    return db_itinerary

def get_itinerary(db: Session, itinerary_id: int):
    return db.query(models.Itinerary).filter(models.Itinerary.id == itinerary_id).first()

def get_itineraries_by_region(db: Session, region_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Itinerary).filter(models.Itinerary.region_id == region_id).offset(skip).limit(limit).all()

def get_itineraries_by_duration(db: Session, duration_nights: int, skip: int = 0, limit: int = 100):
    return db.query(models.Itinerary).filter(models.Itinerary.duration_nights == duration_nights).offset(skip).limit(limit).all() 