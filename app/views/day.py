from sqlite3 import IntegrityError
from fastapi import Depends, HTTPException, Query, Body
from sqlalchemy.orm import Session
from typing import List, Optional
from .base import BaseView
from .. import schemas, crud
from ..database import get_db
from sqlalchemy import and_
from ..models import DayTransfer

class DayView(BaseView):
    """
    API endpoints for managing days in itineraries.
    
    This view provides endpoints for creating, reading, updating, and deleting days,
    as well as managing activities within days.
    """
    
    def setup_routes(self):
        @self.router.post("/", response_model=schemas.Day)
        def create_day(day: schemas.DayCreate, db: Session = Depends(get_db)):
            try:
                # Verify itinerary exists
                if not crud.get_itinerary(db, itinerary_id=day.itinerary_id):
                    self.handle_not_found(day.itinerary_id, "Itinerary")
                
                # Verify hotel exists
                if not crud.get_hotel(db, hotel_id=day.hotel_id):
                    self.handle_not_found(day.hotel_id, "Hotel")
                
                return self.crud.create_day(db=db, day_data=day.model_dump())
            except IntegrityError as e:
                self.handle_integrity_error(e)

        @self.router.get("/", response_model=List[schemas.Day])
        def read_days(
            skip: int = Query(0, ge=0, description="Number of records to skip"),
            limit: int = Query(100, ge=1, le=100, description="Maximum number of records to return"),
            itinerary_id: Optional[int] = Query(None, description="Filter by itinerary ID"),
            hotel_id: Optional[int] = Query(None, description="Filter by hotel ID"),
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
            activity_ids: List[int] = Body(...),
            db: Session = Depends(get_db)
        ):
            """
            Add activities to a specific day.
            
            Args:
                day_id (int): The ID of the day
                activity_ids (List[int]): List of activity IDs to add
                db (Session): Database session
                
            Returns:
                List[DayActivity]: List of created day activities
                
            Raises:
                HTTPException: If the day or any activity doesn't exist
            """
            try:
                day = self.crud.get_day(db, day_id=day_id)
                if not day:
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

        @self.router.get("/{day_id}/transfers", response_model=List[schemas.DayTransfer])
        def get_day_transfers(day_id: int, db: Session = Depends(get_db)):
            """
            Get all transfers for a specific day.
            
            Args:
                day_id (int): The ID of the day
                db (Session): Database session
                
            Returns:
                List[DayTransfer]: List of transfers for the day
                
            Raises:
                HTTPException: If the day doesn't exist
            """
            if not self.crud.get_day(db, day_id=day_id):
                self.handle_not_found(day_id, "Day")
            return crud.get_day_transfers(db, day_id=day_id)

        @self.router.post("/{day_id}/transfers", response_model=List[schemas.DayTransfer])
        def add_transfers_to_day(
            day_id: int,
            transfer_ids: List[int] = Body(...),
            db: Session = Depends(get_db)
        ):
            """
            Add transfers to a specific day.
            
            Args:
                day_id (int): The ID of the day
                transfer_ids (List[int]): List of transfer IDs to add
                db (Session): Database session
                
            Returns:
                List[DayTransfer]: List of created day transfers
                
            Raises:
                HTTPException: If the day or any transfer doesn't exist
            """
            try:
                if not self.crud.get_day(db, day_id=day_id):
                    self.handle_not_found(day_id, "Day")
                
                for transfer_id in transfer_ids:
                    if not crud.get_transfer(db, transfer_id=transfer_id):
                        self.handle_not_found(transfer_id, "Transfer")
                
                created_day_transfers = []
                for transfer_id in transfer_ids:
                    day_transfer = crud.create_day_transfer(db, {
                        "day_id": day_id,
                        "transfer_id": transfer_id
                    })
                    created_day_transfers.append(day_transfer)
                return created_day_transfers
            except IntegrityError as e:
                self.handle_integrity_error(e)

        @self.router.delete("/{day_id}/transfers/{transfer_id}")
        def remove_transfer_from_day(
            day_id: int,
            transfer_id: int,
            db: Session = Depends(get_db)
        ):
            """
            Remove a transfer from a day.
            
            Args:
                day_id (int): The ID of the day
                transfer_id (int): The ID of the transfer to remove
                db (Session): Database session
                
            Returns:
                dict: Success message
                
            Raises:
                HTTPException: If the day or transfer doesn't exist
            """
            if not self.crud.get_day(db, day_id=day_id):
                self.handle_not_found(day_id, "Day")
            if not crud.get_transfer(db, transfer_id=transfer_id):
                self.handle_not_found(transfer_id, "Transfer")
            
            day_transfer = db.query(DayTransfer)\
                .filter(
                    and_(
                        DayTransfer.day_id == day_id,
                        DayTransfer.transfer_id == transfer_id
                    )
                )\
                .first()
            
            if not day_transfer:
                raise HTTPException(
                    status_code=404,
                    detail=f"Transfer {transfer_id} not found in day {day_id}"
                )
            
            db.delete(day_transfer)
            db.commit()
            return {"message": "Transfer removed from day successfully"} 