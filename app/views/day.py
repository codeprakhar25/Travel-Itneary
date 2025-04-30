from fastapi import Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from .base import BaseView
from .. import schemas, crud
from ..database import get_db

class DayView(BaseView):
    def setup_routes(self):
        @self.router.post("/", response_model=schemas.Day)
        def create_day(day: schemas.DayCreate, db: Session = Depends(get_db)):
            try:
                if not crud.get_itinerary(db, itinerary_id=day.itinerary_id):
                    self.handle_not_found(day.itinerary_id, "Itinerary")
                if not crud.get_hotel(db, hotel_id=day.hotel_id):
                    self.handle_not_found(day.hotel_id, "Hotel")
                return self.crud.create_day(db=db, day_data=day.model_dump())
            except IntegrityError as e:
                self.handle_integrity_error(e)

        @self.router.get("/", response_model=List[schemas.Day])
        def read_days(
            skip: int = Query(0, ge=0),
            limit: int = Query(100, ge=1, le=100),
            itinerary_id: Optional[int] = None,
            hotel_id: Optional[int] = None,
            db: Session = Depends(get_db)
        ):
            return self.crud.get_days(
                db,
                skip=skip,
                limit=limit,
                itinerary_id=itinerary_id,
                hotel_id=hotel_id
            )

        @self.router.get("/{day_id}", response_model=schemas.Day)
        def read_day(day_id: int, db: Session = Depends(get_db)):
            db_day = self.crud.get_day(db, day_id=day_id)
            if not db_day:
                self.handle_not_found(day_id, "Day")
            return db_day

        @self.router.put("/{day_id}", response_model=schemas.Day)
        def update_day(day_id: int, day: schemas.DayUpdate, db: Session = Depends(get_db)):
            try:
                if not self.crud.get_day(db, day_id=day_id):
                    self.handle_not_found(day_id, "Day")
                if day.hotel_id and not crud.get_hotel(db, hotel_id=day.hotel_id):
                    self.handle_not_found(day.hotel_id, "Hotel")
                return self.crud.update_day(db, day_id=day_id, day_data=day.model_dump(exclude_unset=True))
            except IntegrityError as e:
                self.handle_integrity_error(e)

        @self.router.delete("/{day_id}")
        def delete_day(day_id: int, db: Session = Depends(get_db)):
            db_day = self.crud.delete_day(db, day_id=day_id)
            if not db_day:
                self.handle_not_found(day_id, "Day")
            return {"message": "Day deleted successfully"}

        @self.router.get("/{day_id}/activities", response_model=List[schemas.DayActivity])
        def get_day_activities(day_id: int, db: Session = Depends(get_db)):
            if not self.crud.get_day(db, day_id=day_id):
                self.handle_not_found(day_id, "Day")
            return crud.get_day_activities(db, day_id=day_id)

        @self.router.post("/{day_id}/activities", response_model=List[schemas.DayActivity])
        def add_activities_to_day(
            day_id: int,
            activity_ids: List[int],
            db: Session = Depends(get_db)
        ):
            try:
                if not self.crud.get_day(db, day_id=day_id):
                    self.handle_not_found(day_id, "Day")
                
                for activity_id in activity_ids:
                    if not crud.get_activity(db, activity_id=activity_id):
                        self.handle_not_found(activity_id, "Activity")
                
                created_day_activities = []
                for activity_id in activity_ids:
                    day_activity = crud.create_day_activity(db, {
                        "day_id": day_id,
                        "activity_id": activity_id
                    })
                    created_day_activities.append(day_activity)
                return created_day_activities
            except IntegrityError as e:
                self.handle_integrity_error(e) 