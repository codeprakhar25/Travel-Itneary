from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from .models import LocationType, AccommodationType, TransferType, ActivityType

class RegionBase(BaseModel):
    name: str
    description: Optional[str] = None

class RegionCreate(RegionBase):
    pass

class RegionUpdate(RegionBase):
    name: Optional[str] = None

class Region(RegionBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class HotelBase(BaseModel):
    name: str
    location: str
    location_type: LocationType
    rating: float
    price_per_night: float
    region_id: int

class HotelCreate(HotelBase):
    pass

class HotelUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    location_type: Optional[LocationType] = None
    rating: Optional[float] = None
    price_per_night: Optional[float] = None
    region_id: Optional[int] = None

class Hotel(HotelBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class ActivityBase(BaseModel):
    name: str
    description: str
    duration_hours: float
    price: float

class ActivityCreate(ActivityBase):
    pass

class ActivityUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    duration_hours: Optional[float] = None
    price: Optional[float] = None

class Activity(ActivityBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

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

class TransferUpdate(BaseModel):
    from_location: Optional[str] = None
    to_location: Optional[str] = None
    mode: Optional[str] = None
    duration_minutes: Optional[int] = None
    price: Optional[float] = None

class Transfer(TransferBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class DayActivityBase(BaseModel):
    day_id: int
    activity_id: int

class DayActivityCreate(DayActivityBase):
    pass

class DayActivity(DayActivityBase):
    id: int
    created_at: datetime
    activity: Activity

    class Config:
        from_attributes = True

class DayBase(BaseModel):
    day_number: int
    hotel_id: int

class DayCreate(DayBase):
    pass

class DayUpdate(BaseModel):
    day_number: Optional[int] = None
    hotel_id: Optional[int] = None

class Day(DayBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    hotel: Hotel
    activities: List[DayActivity]

    class Config:
        from_attributes = True

class DayTransferBase(BaseModel):
    day_id: int
    transfer_id: int

class DayTransferCreate(DayTransferBase):
    pass

class DayTransfer(DayTransferBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class ItineraryBase(BaseModel):
    title: str
    description: Optional[str] = None
    duration_nights: int
    region_id: int

class ItineraryCreate(ItineraryBase):
    pass

class ItineraryUpdate(ItineraryBase):
    title: Optional[str] = None
    description: Optional[str] = None
    duration_nights: Optional[int] = None
    region_id: Optional[int] = None

class Itinerary(ItineraryBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    region: Region
    days: List[Day]

    class Config:
        from_attributes = True 