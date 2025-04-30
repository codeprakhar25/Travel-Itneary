from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_
from . import models, schemas
from typing import List, Optional
from datetime import datetime
from .models import LocationType

def create_region(db: Session, region_data: dict):
    db_region = models.Region(**region_data)
    db.add(db_region)
    db.commit()
    db.refresh(db_region)
    return db_region

def get_region(db: Session, region_id: int):
    return db.query(models.Region).filter(models.Region.id == region_id).first()

def get_regions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Region).offset(skip).limit(limit).all()

def update_region(db: Session, region_id: int, region_data: dict):
    db_region = db.query(models.Region).filter(models.Region.id == region_id).first()
    if db_region:
        for key, value in region_data.items():
            setattr(db_region, key, value)
        db.commit()
        db.refresh(db_region)
    return db_region

def delete_region(db: Session, region_id: int):
    db_region = db.query(models.Region).filter(models.Region.id == region_id).first()
    if db_region:
        db.delete(db_region)
        db.commit()
    return db_region

def create_hotel(db: Session, hotel_data: dict):
    db_hotel = models.Hotel(
        name=hotel_data["name"],
        location=hotel_data["location"],
        location_type=hotel_data["location_type"],
        rating=hotel_data["rating"],
        price_per_night=hotel_data["price_per_night"],
        region_id=hotel_data["region_id"]
    )
    db.add(db_hotel)
    db.commit()
    db.refresh(db_hotel)
    return db_hotel

def get_hotel(db: Session, hotel_id: int):
    return db.query(models.Hotel).filter(models.Hotel.id == hotel_id).first()

def get_hotels(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    region_id: Optional[int] = None,
    location_type: Optional[LocationType] = None,
    min_rating: Optional[float] = None,
    max_price: Optional[float] = None
):
    query = db.query(models.Hotel)
    
    if region_id:
        query = query.filter(models.Hotel.region_id == region_id)
    if location_type:
        query = query.filter(models.Hotel.location_type == location_type)
    if min_rating:
        query = query.filter(models.Hotel.rating >= min_rating)
    if max_price:
        query = query.filter(models.Hotel.price_per_night <= max_price)
    
    return query.offset(skip).limit(limit).all()

def get_hotels_by_region(db: Session, region_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Hotel).filter(models.Hotel.region_id == region_id).offset(skip).limit(limit).all()

def update_hotel(db: Session, hotel_id: int, hotel_data: dict):
    db_hotel = db.query(models.Hotel).filter(models.Hotel.id == hotel_id).first()
    if db_hotel:
        for key, value in hotel_data.items():
            setattr(db_hotel, key, value)
        db.commit()
        db.refresh(db_hotel)
    return db_hotel

def delete_hotel(db: Session, hotel_id: int):
    db_hotel = db.query(models.Hotel).filter(models.Hotel.id == hotel_id).first()
    if db_hotel:
        db.delete(db_hotel)
        db.commit()
    return db_hotel

def create_activity(db: Session, activity_data: dict):
    db_activity = models.Activity(**activity_data)
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    return db_activity

def get_activity(db: Session, activity_id: int):
    return db.query(models.Activity).filter(models.Activity.id == activity_id).first()

def get_activities(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    min_duration: Optional[float] = None,
    max_price: Optional[float] = None
):
    query = db.query(models.Activity)
    
    if min_duration:
        query = query.filter(models.Activity.duration_hours >= min_duration)
    if max_price:
        query = query.filter(models.Activity.price <= max_price)
    
    return query.offset(skip).limit(limit).all()

def update_activity(db: Session, activity_id: int, activity_data: dict):
    db_activity = db.query(models.Activity).filter(models.Activity.id == activity_id).first()
    if db_activity:
        for key, value in activity_data.items():
            setattr(db_activity, key, value)
        db.commit()
        db.refresh(db_activity)
    return db_activity

def delete_activity(db: Session, activity_id: int):
    db_activity = db.query(models.Activity).filter(models.Activity.id == activity_id).first()
    if db_activity:
        db.delete(db_activity)
        db.commit()
    return db_activity

def create_transfer(db: Session, transfer_data: dict):
    db_transfer = models.Transfer(**transfer_data)
    db.add(db_transfer)
    db.commit()
    db.refresh(db_transfer)
    return db_transfer

def get_transfer(db: Session, transfer_id: int):
    return db.query(models.Transfer).filter(models.Transfer.id == transfer_id).first()

def get_transfers(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    from_location: Optional[str] = None,
    to_location: Optional[str] = None,
    max_duration: Optional[int] = None,
    max_price: Optional[float] = None
):
    query = db.query(models.Transfer)
    
    if from_location:
        query = query.filter(models.Transfer.from_location == from_location)
    if to_location:
        query = query.filter(models.Transfer.to_location == to_location)
    if max_duration:
        query = query.filter(models.Transfer.duration_minutes <= max_duration)
    if max_price:
        query = query.filter(models.Transfer.price <= max_price)
    
    return query.offset(skip).limit(limit).all()

def update_transfer(db: Session, transfer_id: int, transfer_data: dict):
    db_transfer = db.query(models.Transfer).filter(models.Transfer.id == transfer_id).first()
    if db_transfer:
        for key, value in transfer_data.items():
            setattr(db_transfer, key, value)
        db.commit()
        db.refresh(db_transfer)
    return db_transfer

def delete_transfer(db: Session, transfer_id: int):
    db_transfer = db.query(models.Transfer).filter(models.Transfer.id == transfer_id).first()
    if db_transfer:
        db.delete(db_transfer)
        db.commit()
    return db_transfer

def create_day(db: Session, day_data: dict):
    db_day = models.Day(**day_data)
    db.add(db_day)
    db.commit()
    db.refresh(db_day)
    return db_day

def get_day(db: Session, day_id: int):
    return db.query(models.Day).filter(models.Day.id == day_id).first()

def get_days_by_itinerary(db: Session, itinerary_id: int):
    return db.query(models.Day).filter(models.Day.itinerary_id == itinerary_id).all()

def update_day(db: Session, day_id: int, day_data: dict):
    db_day = db.query(models.Day).filter(models.Day.id == day_id).first()
    if db_day:
        for key, value in day_data.items():
            setattr(db_day, key, value)
        db.commit()
        db.refresh(db_day)
    return db_day

def delete_day(db: Session, day_id: int):
    db_day = db.query(models.Day).filter(models.Day.id == day_id).first()
    if db_day:
        db.delete(db_day)
        db.commit()
    return db_day

def create_day_activity(db: Session, day_activity_data: dict):
    db_day_activity = models.DayActivity(**day_activity_data)
    db.add(db_day_activity)
    db.commit()
    db.refresh(db_day_activity)
    return db_day_activity

def get_day_activities(db: Session, day_id: int):
    return db.query(models.DayActivity).filter(models.DayActivity.day_id == day_id).all()

def delete_day_activity(db: Session, day_activity_id: int):
    db_day_activity = db.query(models.DayActivity).filter(models.DayActivity.id == day_activity_id).first()
    if db_day_activity:
        db.delete(db_day_activity)
        db.commit()
    return db_day_activity

def create_day_transfer(db: Session, day_transfer_data: dict):
    db_day_transfer = models.DayTransfer(**day_transfer_data)
    db.add(db_day_transfer)
    db.commit()
    db.refresh(db_day_transfer)
    return db_day_transfer

def get_day_transfers(db: Session, day_id: int):
    return db.query(models.DayTransfer).filter(models.DayTransfer.day_id == day_id).all()

def delete_day_transfer(db: Session, day_transfer_id: int):
    db_day_transfer = db.query(models.DayTransfer).filter(models.DayTransfer.id == day_transfer_id).first()
    if db_day_transfer:
        db.delete(db_day_transfer)
        db.commit()
    return db_day_transfer

def create_itinerary(db: Session, itinerary_data: dict):
    db_itinerary = models.Itinerary(**itinerary_data)
    db.add(db_itinerary)
    db.commit()
    db.refresh(db_itinerary)
    return db_itinerary

def get_itinerary(db: Session, itinerary_id: int):
    return db.query(models.Itinerary)\
        .options(
            joinedload(models.Itinerary.region),
            joinedload(models.Itinerary.days)
            .joinedload(models.Day.hotel),
            joinedload(models.Itinerary.days)
            .joinedload(models.Day.activities)
            .joinedload(models.DayActivity.activity)
        )\
        .filter(models.Itinerary.id == itinerary_id)\
        .first()

def get_itineraries(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    region_id: Optional[int] = None,
    duration_nights: Optional[int] = None
):
    query = db.query(models.Itinerary)
    
    if region_id:
        query = query.filter(models.Itinerary.region_id == region_id)
    if duration_nights:
        query = query.filter(models.Itinerary.duration_nights == duration_nights)
    
    return query.offset(skip).limit(limit).all()

def get_itineraries_by_region(db: Session, region_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Itinerary).filter(models.Itinerary.region_id == region_id).offset(skip).limit(limit).all()

def get_itineraries_by_duration(db: Session, duration_nights: int, skip: int = 0, limit: int = 100):
    return db.query(models.Itinerary).filter(models.Itinerary.duration_nights == duration_nights).offset(skip).limit(limit).all()

def update_itinerary(db: Session, itinerary_id: int, itinerary_data: dict):
    db_itinerary = db.query(models.Itinerary).filter(models.Itinerary.id == itinerary_id).first()
    if db_itinerary:
        for key, value in itinerary_data.items():
            setattr(db_itinerary, key, value)
        db.commit()
        db.refresh(db_itinerary)
    return db_itinerary

def delete_itinerary(db: Session, itinerary_id: int):
    db_itinerary = db.query(models.Itinerary).filter(models.Itinerary.id == itinerary_id).first()
    if db_itinerary:
        db.delete(db_itinerary)
        db.commit()
    return db_itinerary

def get_recommended_itineraries(
    db: Session,
    duration_nights: int,
    limit: int = 5,
    min_activities_per_day: int = 1,
    max_activities_per_day: int = 3
):
    """
    Get recommended itineraries based on duration and activity mix.
    
    Args:
        db (Session): Database session
        duration_nights (int): Number of nights for the itinerary
        limit (int): Maximum number of recommendations to return
        min_activities_per_day (int): Minimum number of activities per day
        max_activities_per_day (int): Maximum number of activities per day
        
    Returns:
        List[Itinerary]: List of recommended itineraries
    """
    # Get all itineraries with the specified duration
    itineraries = db.query(models.Itinerary)\
        .filter(models.Itinerary.duration_nights == duration_nights)\
        .options(
            joinedload(models.Itinerary.days)
            .joinedload(models.Day.activities)
            .joinedload(models.DayActivity.activity)
        )\
        .all()
    
    # Filter itineraries based on activity mix and transfer availability
    valid_itineraries = []
    for itinerary in itineraries:
        # Check if each day has the right number of activities
        valid_activity_mix = True
        for day in itinerary.days:
            activity_count = len(day.activities)
            if activity_count < min_activities_per_day or activity_count > max_activities_per_day:
                valid_activity_mix = False
                break
        
        if not valid_activity_mix:
            continue
            
        # Check if transfers are available between locations
        valid_transfers = True
        for i in range(len(itinerary.days) - 1):
            current_hotel = itinerary.days[i].hotel
            next_hotel = itinerary.days[i + 1].hotel
            
            # Check if there's a transfer between these locations
            transfer = db.query(models.Transfer)\
                .filter(
                    and_(
                        models.Transfer.from_location == current_hotel.location,
                        models.Transfer.to_location == next_hotel.location
                    )
                )\
                .first()
                
            if not transfer:
                valid_transfers = False
                break
        
        if valid_transfers:
            valid_itineraries.append(itinerary)
    
    # Sort by rating and return top recommendations
    valid_itineraries.sort(key=lambda x: x.rating, reverse=True)
    return valid_itineraries[:limit]

def get_days(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    itinerary_id: Optional[int] = None,
    hotel_id: Optional[int] = None
):
    query = db.query(models.Day)
    
    if itinerary_id:
        query = query.filter(models.Day.itinerary_id == itinerary_id)
    if hotel_id:
        query = query.filter(models.Day.hotel_id == hotel_id)
    
    return query.offset(skip).limit(limit).all() 