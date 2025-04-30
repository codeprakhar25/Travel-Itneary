from sqlite3 import IntegrityError
from fastapi import Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from .base import BaseView
from .. import schemas, crud
from ..database import get_db

class ItineraryView(BaseView):
    """
    API endpoints for managing travel itineraries.
    
    This view provides endpoints for creating, reading, updating, and deleting itineraries,
    as well as managing days and activities within itineraries.
    """
    
    def setup_routes(self):
        @self.router.post("/", response_model=schemas.Itinerary)
        def create_itinerary(itinerary: schemas.ItineraryCreate, db: Session = Depends(get_db)):
            """
            Create a new itinerary.
            
            Args:
                itinerary (ItineraryCreate): The itinerary data to create
                db (Session): Database session
                
            Returns:
                Itinerary: The created itinerary
                
            Raises:
                HTTPException: If the region doesn't exist or there's an integrity error
            """
            try:
                if not crud.get_region(db, region_id=itinerary.region_id):
                    self.handle_not_found(itinerary.region_id, "Region")
                return self.crud.create_itinerary(db=db, itinerary_data=itinerary.model_dump())
            except IntegrityError as e:
                self.handle_integrity_error(e)

        @self.router.get("/", response_model=List[schemas.Itinerary])
        def read_itineraries(
            skip: int = Query(0, ge=0, description="Number of records to skip"),
            limit: int = Query(100, ge=1, le=100, description="Maximum number of records to return"),
            region_id: Optional[int] = Query(None, description="Filter by region ID"),
            duration_nights: Optional[int] = Query(None, description="Filter by duration in nights"),
            db: Session = Depends(get_db)
        ):
            """
            Get a list of itineraries with optional filtering.
            
            Args:
                skip (int): Number of records to skip (for pagination)
                limit (int): Maximum number of records to return
                region_id (Optional[int]): Filter by region ID
                duration_nights (Optional[int]): Filter by duration in nights
                db (Session): Database session
                
            Returns:
                List[Itinerary]: List of itineraries matching the criteria
            """
            return self.crud.get_itineraries(
                db,
                skip=skip,
                limit=limit,
                region_id=region_id,
                duration_nights=duration_nights
            )

        @self.router.get("/{itinerary_id}", response_model=schemas.Itinerary)
        def read_itinerary(itinerary_id: int, db: Session = Depends(get_db)):
            """
            Get a specific itinerary by ID.
            
            Args:
                itinerary_id (int): The ID of the itinerary to retrieve
                db (Session): Database session
                
            Returns:
                Itinerary: The requested itinerary
                
            Raises:
                HTTPException: If the itinerary doesn't exist
            """
            db_itinerary = self.crud.get_itinerary(db, itinerary_id=itinerary_id)
            if not db_itinerary:
                self.handle_not_found(itinerary_id, "Itinerary")
            return db_itinerary

        @self.router.put("/{itinerary_id}", response_model=schemas.Itinerary)
        def update_itinerary(itinerary_id: int, itinerary: schemas.ItineraryUpdate, db: Session = Depends(get_db)):
            """
            Update an existing itinerary.
            
            Args:
                itinerary_id (int): The ID of the itinerary to update
                itinerary (ItineraryUpdate): The updated itinerary data
                db (Session): Database session
                
            Returns:
                Itinerary: The updated itinerary
                
            Raises:
                HTTPException: If the itinerary doesn't exist or there's an integrity error
            """
            try:
                if not self.crud.get_itinerary(db, itinerary_id=itinerary_id):
                    self.handle_not_found(itinerary_id, "Itinerary")
                if itinerary.region_id and not crud.get_region(db, region_id=itinerary.region_id):
                    self.handle_not_found(itinerary.region_id, "Region")
                return self.crud.update_itinerary(db, itinerary_id=itinerary_id, itinerary_data=itinerary.model_dump(exclude_unset=True))
            except IntegrityError as e:
                self.handle_integrity_error(e)

        @self.router.delete("/{itinerary_id}")
        def delete_itinerary(itinerary_id: int, db: Session = Depends(get_db)):
            """
            Delete an itinerary.
            
            Args:
                itinerary_id (int): The ID of the itinerary to delete
                db (Session): Database session
                
            Returns:
                dict: Success message
                
            Raises:
                HTTPException: If the itinerary doesn't exist
            """
            db_itinerary = self.crud.delete_itinerary(db, itinerary_id=itinerary_id)
            if not db_itinerary:
                self.handle_not_found(itinerary_id, "Itinerary")
            return {"message": "Itinerary deleted successfully"}

        @self.router.post("/{itinerary_id}/days", response_model=List[schemas.Day])
        def add_days_to_itinerary(
            itinerary_id: int,
            days_data: List[schemas.DayCreate],
            db: Session = Depends(get_db)
        ):
            """
            Add multiple days to an itinerary.
            
            Args:
                itinerary_id (int): The ID of the itinerary
                days_data (List[DayCreate]): List of day data to create
                db (Session): Database session
                
            Returns:
                List[Day]: List of created days
                
            Raises:
                HTTPException: If the itinerary or any hotel doesn't exist
            """
            try:
                if not self.crud.get_itinerary(db, itinerary_id=itinerary_id):
                    self.handle_not_found(itinerary_id, "Itinerary")
                
                for day_data in days_data:
                    if not crud.get_hotel(db, hotel_id=day_data.hotel_id):
                        self.handle_not_found(day_data.hotel_id, "Hotel")
                
                created_days = []
                for day_data in days_data:
                    day_data_dict = day_data.model_dump()
                    day_data_dict["itinerary_id"] = itinerary_id
                    day = crud.create_day(db, day_data=day_data_dict)
                    created_days.append(day)
                return created_days
            except IntegrityError as e:
                self.handle_integrity_error(e)

        @self.router.post("/{itinerary_id}/days/{day_id}/activities", response_model=List[schemas.DayActivity])
        def add_activities_to_day(
            itinerary_id: int,
            day_id: int,
            activity_ids: List[int],
            db: Session = Depends(get_db)
        ):
            try:
                if not self.crud.get_itinerary(db, itinerary_id=itinerary_id):
                    self.handle_not_found(itinerary_id, "Itinerary")
                
                day = crud.get_day(db, day_id=day_id)
                if not day or day.itinerary_id != itinerary_id:
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

        @self.router.get("/{itinerary_id}/days", response_model=List[schemas.Day])
        def get_itinerary_days(itinerary_id: int, db: Session = Depends(get_db)):
            """
            Get all days for an itinerary.
            
            Args:
                itinerary_id (int): The ID of the itinerary
                db (Session): Database session
                
            Returns:
                List[Day]: List of days in the itinerary
                
            Raises:
                HTTPException: If the itinerary doesn't exist
            """
            if not self.crud.get_itinerary(db, itinerary_id=itinerary_id):
                self.handle_not_found(itinerary_id, "Itinerary")
            return crud.get_days_by_itinerary(db, itinerary_id=itinerary_id) 