from fastapi import Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from .base import BaseView
from .. import schemas, crud
from ..database import get_db
from ..models import LocationType

class HotelView(BaseView):
    def setup_routes(self):
        @self.router.post("/", response_model=schemas.Hotel)
        def create_hotel(hotel: schemas.HotelCreate, db: Session = Depends(get_db)):
            try:
                if not crud.get_region(db, region_id=hotel.region_id):
                    self.handle_not_found(hotel.region_id, "Region")
                return self.crud.create_hotel(db=db, hotel_data=hotel.model_dump())
            except DataError as e:
                if "locationtype" in str(e).lower():
                    valid_types = [t.value for t in LocationType]
                    raise HTTPException(
                        status_code=400,
                        detail=f"Invalid location type. Valid types are: {', '.join(valid_types)}"
                    )
                raise HTTPException(status_code=400, detail=str(e))
            except IntegrityError as e:
                self.handle_integrity_error(e, f"Region with id {hotel.region_id} does not exist")

        @self.router.get("/", response_model=List[schemas.Hotel])
        def read_hotels(
            skip: int = Query(0, ge=0),
            limit: int = Query(100, ge=1, le=100),
            region_id: Optional[int] = None,
            location_type: Optional[LocationType] = None,
            min_rating: Optional[float] = None,
            max_price: Optional[float] = None,
            db: Session = Depends(get_db)
        ):
            return self.crud.get_hotels(
                db,
                skip=skip,
                limit=limit,
                region_id=region_id,
                location_type=location_type,
                min_rating=min_rating,
                max_price=max_price
            )

        @self.router.get("/{hotel_id}", response_model=schemas.Hotel)
        def read_hotel(hotel_id: int, db: Session = Depends(get_db)):
            db_hotel = self.crud.get_hotel(db, hotel_id=hotel_id)
            if not db_hotel:
                self.handle_not_found(hotel_id, "Hotel")
            return db_hotel

        @self.router.put("/{hotel_id}", response_model=schemas.Hotel)
        def update_hotel(hotel_id: int, hotel: schemas.HotelUpdate, db: Session = Depends(get_db)):
            try:
                if not self.crud.get_hotel(db, hotel_id=hotel_id):
                    self.handle_not_found(hotel_id, "Hotel")
                if hotel.region_id and not crud.get_region(db, region_id=hotel.region_id):
                    self.handle_not_found(hotel.region_id, "Region")
                return self.crud.update_hotel(db, hotel_id=hotel_id, hotel_data=hotel.model_dump(exclude_unset=True))
            except DataError as e:
                if "locationtype" in str(e).lower():
                    valid_types = [t.value for t in LocationType]
                    raise HTTPException(
                        status_code=400,
                        detail=f"Invalid location type. Valid types are: {', '.join(valid_types)}"
                    )
                raise HTTPException(status_code=400, detail=str(e))
            except IntegrityError as e:
                self.handle_integrity_error(e)

        @self.router.delete("/{hotel_id}")
        def delete_hotel(hotel_id: int, db: Session = Depends(get_db)):
            db_hotel = self.crud.delete_hotel(db, hotel_id=hotel_id)
            if not db_hotel:
                self.handle_not_found(hotel_id, "Hotel")
            return {"message": "Hotel deleted successfully"} 