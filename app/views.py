from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Type
from . import crud, schemas
from .database import get_db

class BaseView:
    def __init__(self, model: Type[schemas.BaseModel], crud_module):
        self.model = model
        self.crud = crud_module
        self.router = APIRouter()
        self.setup_routes()

class RegionView(BaseView):
    def setup_routes(self):
        @self.router.post("/", response_model=schemas.Region)
        def create_region(region: schemas.RegionCreate, db: Session = Depends(get_db)):
            return self.crud.create_region(db=db, region=region)

        @self.router.get("/{region_id}", response_model=schemas.Region)
        def read_region(region_id: int, db: Session = Depends(get_db)):
            db_region = self.crud.get_region(db, region_id=region_id)
            if db_region is None:
                raise HTTPException(status_code=404, detail="Region not found")
            return db_region

class HotelView(BaseView):
    def setup_routes(self):
        @self.router.post("/", response_model=schemas.Hotel)
        def create_hotel(hotel: schemas.HotelCreate, db: Session = Depends(get_db)):
            return self.crud.create_hotel(db=db, hotel=hotel)

        @self.router.get("/{hotel_id}", response_model=schemas.Hotel)
        def read_hotel(hotel_id: int, db: Session = Depends(get_db)):
            db_hotel = self.crud.get_hotel(db, hotel_id=hotel_id)
            if db_hotel is None:
                raise HTTPException(status_code=404, detail="Hotel not found")
            return db_hotel

class ItineraryView(BaseView):
    def setup_routes(self):
        @self.router.post("/", response_model=schemas.Itinerary)
        def create_itinerary(itinerary: schemas.ItineraryCreate, db: Session = Depends(get_db)):
            return self.crud.create_itinerary(db=db, itinerary=itinerary)

        @self.router.get("/{itinerary_id}", response_model=schemas.Itinerary)
        def read_itinerary(itinerary_id: int, db: Session = Depends(get_db)):
            db_itinerary = self.crud.get_itinerary(db, itinerary_id=itinerary_id)
            if db_itinerary is None:
                raise HTTPException(status_code=404, detail="Itinerary not found")
            return db_itinerary

        @self.router.get("/regions/{region_id}/", response_model=List[schemas.Itinerary])
        def read_region_itineraries(region_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
            itineraries = self.crud.get_itineraries_by_region(db, region_id=region_id, skip=skip, limit=limit)
            return itineraries

        @self.router.get("/duration/{duration_nights}", response_model=List[schemas.Itinerary])
        def read_itineraries_by_duration(duration_nights: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
            itineraries = self.crud.get_itineraries_by_duration(db, duration_nights=duration_nights, skip=skip, limit=limit)
            return itineraries 