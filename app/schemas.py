from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class RegionBase(BaseModel):
    name: str
    description: Optional[str] = None

class RegionCreate(RegionBase):
    pass

class Region(RegionBase):
    id: int
    class Config:
        from_attributes = True

class HotelBase(BaseModel):
    name: str
    location: str
    rating: float
    price_per_night: float

class HotelCreate(HotelBase):
    pass

class Hotel(HotelBase):
    id: int
    class Config:
        from_attributes = True

class ActivityBase(BaseModel):
    name: str
    description: str
    duration_hours: float
    price: float

class ActivityCreate(ActivityBase):
    pass

class Activity(ActivityBase):
    id: int
    class Config:
        from_attributes = True

class TransferBase(BaseModel):
    from_location: str
    to_location: str
    mode: str
    duration_minutes: int
    price: float

class TransferCreate(TransferBase):
    pass

class Transfer(TransferBase):
    id: int
    class Config:
        from_attributes = True

class DayBase(BaseModel):
    day_number: int
    hotel_id: int

class DayCreate(DayBase):
    activities: List[ActivityCreate] = []
    transfers: List[TransferCreate] = []

class Day(DayBase):
    id: int
    activities: List[Activity] = []
    transfers: List[Transfer] = []
    class Config:
        from_attributes = True

class ItineraryBase(BaseModel):
    title: str
    duration_nights: int
    region_id: int

class ItineraryCreate(ItineraryBase):
    days: List[DayCreate] = []

class Itinerary(ItineraryBase):
    id: int
    created_at: datetime
    days: List[Day] = []
    class Config:
        from_attributes = True 