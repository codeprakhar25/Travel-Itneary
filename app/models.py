import enum
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Table, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class LocationType(enum.Enum):
    CITY = "city"
    BEACH = "beach"
    ISLAND = "island"
    MOUNTAIN = "mountain"
    LANDMARK = "landmark"

class AccommodationType(enum.Enum):
    HOTEL = "hotel"
    RESORT = "resort"
    VILLA = "villa"
    HOSTEL = "hostel"
    GUESTHOUSE = "guesthouse"

class TransferType(enum.Enum):
    PRIVATE_CAR = "private_car"
    SHARED_VAN = "shared_van"
    FERRY = "ferry"
    SPEEDBOAT = "speedboat"
    FLIGHT = "flight"
    BUS = "bus"

class ActivityType(enum.Enum):
    SIGHTSEEING = "sightseeing"
    ADVENTURE = "adventure"
    CULTURAL = "cultural"
    FOOD = "food"
    RELAXATION = "relaxation"
    WATER_SPORT = "water_sport"


class Region(Base):
    __tablename__ = "regions"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    hotels = relationship("Hotel", back_populates="region")
    itineraries = relationship("Itinerary", back_populates="region")

class Hotel(Base):
    __tablename__ = "hotels"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    location = Column(String, nullable=False)
    location_type = Column(Enum(LocationType), nullable=False)
    rating = Column(Float, nullable=False)
    price_per_night = Column(Float, nullable=False)
    region_id = Column(Integer, ForeignKey("regions.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    region = relationship("Region", back_populates="hotels")
    days = relationship("Day", back_populates="hotel")

class Activity(Base):
    __tablename__ = "activities"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=False)
    duration_hours = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    days = relationship("DayActivity", back_populates="activity")

class Transfer(Base):
    __tablename__ = "transfers"
    
    id = Column(Integer, primary_key=True, index=True)
    from_location = Column(String, nullable=False)
    to_location = Column(String, nullable=False)
    mode = Column(String, nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    days = relationship("DayTransfer", back_populates="transfer")

class Itinerary(Base):
    __tablename__ = "itineraries"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String)
    duration_nights = Column(Integer, nullable=False)
    region_id = Column(Integer, ForeignKey("regions.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    region = relationship("Region", back_populates="itineraries")
    days = relationship("Day", back_populates="itinerary")

class Day(Base):
    __tablename__ = "days"
    
    id = Column(Integer, primary_key=True, index=True)
    day_number = Column(Integer, nullable=False)
    itinerary_id = Column(Integer, ForeignKey("itineraries.id"), nullable=False)
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    itinerary = relationship("Itinerary", back_populates="days")
    hotel = relationship("Hotel", back_populates="days")
    activities = relationship("DayActivity", back_populates="day")
    transfers = relationship("DayTransfer", back_populates="day")

class DayActivity(Base):
    __tablename__ = "day_activities"
    
    id = Column(Integer, primary_key=True, index=True)
    day_id = Column(Integer, ForeignKey("days.id"), nullable=False)
    activity_id = Column(Integer, ForeignKey("activities.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    day = relationship("Day", back_populates="activities")
    activity = relationship("Activity", back_populates="days")

class DayTransfer(Base):
    __tablename__ = "day_transfers"
    
    id = Column(Integer, primary_key=True, index=True)
    day_id = Column(Integer, ForeignKey("days.id"), nullable=False)
    transfer_id = Column(Integer, ForeignKey("transfers.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    day = relationship("Day", back_populates="transfers")
    transfer = relationship("Transfer", back_populates="days") 