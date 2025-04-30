from fastapi import Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from .base import BaseView
from .. import schemas, crud
from ..database import get_db

class ActivityView(BaseView):
    def setup_routes(self):
        @self.router.post("/", response_model=schemas.Activity)
        def create_activity(activity: schemas.ActivityCreate, db: Session = Depends(get_db)):
            try:
                return self.crud.create_activity(db=db, activity_data=activity.model_dump())
            except IntegrityError as e:
                self.handle_integrity_error(e)

        @self.router.get("/", response_model=List[schemas.Activity])
        def read_activities(
            skip: int = Query(0, ge=0),
            limit: int = Query(100, ge=1, le=100),
            min_duration: Optional[float] = None,
            max_price: Optional[float] = None,
            db: Session = Depends(get_db)
        ):
            return self.crud.get_activities(
                db,
                skip=skip,
                limit=limit,
                min_duration=min_duration,
                max_price=max_price
            )

        @self.router.get("/{activity_id}", response_model=schemas.Activity)
        def read_activity(activity_id: int, db: Session = Depends(get_db)):
            db_activity = self.crud.get_activity(db, activity_id=activity_id)
            if not db_activity:
                self.handle_not_found(activity_id, "Activity")
            return db_activity

        @self.router.put("/{activity_id}", response_model=schemas.Activity)
        def update_activity(activity_id: int, activity: schemas.ActivityUpdate, db: Session = Depends(get_db)):
            try:
                if not self.crud.get_activity(db, activity_id=activity_id):
                    self.handle_not_found(activity_id, "Activity")
                return self.crud.update_activity(db, activity_id=activity_id, activity_data=activity.model_dump(exclude_unset=True))
            except IntegrityError as e:
                self.handle_integrity_error(e)

        @self.router.delete("/{activity_id}")
        def delete_activity(activity_id: int, db: Session = Depends(get_db)):
            db_activity = self.crud.delete_activity(db, activity_id=activity_id)
            if not db_activity:
                self.handle_not_found(activity_id, "Activity")
            return {"message": "Activity deleted successfully"} 