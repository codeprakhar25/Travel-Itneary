from fastapi import Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from .base import BaseView
from .. import schemas, crud
from ..database import get_db

class RegionView(BaseView):
    def setup_routes(self):
        @self.router.post("/", response_model=schemas.Region)
        def create_region(region: schemas.RegionCreate, db: Session = Depends(get_db)):
            try:
                return self.crud.create_region(db=db, region_data=region.model_dump())
            except IntegrityError as e:
                self.handle_integrity_error(e)

        @self.router.get("/", response_model=List[schemas.Region])
        def read_regions(
            skip: int = Query(0, ge=0),
            limit: int = Query(100, ge=1, le=100),
            db: Session = Depends(get_db)
        ):
            return self.crud.get_regions(db, skip=skip, limit=limit)

        @self.router.get("/{region_id}", response_model=schemas.Region)
        def read_region(region_id: int, db: Session = Depends(get_db)):
            db_region = self.crud.get_region(db, region_id=region_id)
            if not db_region:
                self.handle_not_found(region_id, "Region")
            return db_region

        @self.router.put("/{region_id}", response_model=schemas.Region)
        def update_region(region_id: int, region: schemas.RegionUpdate, db: Session = Depends(get_db)):
            try:
                db_region = self.crud.update_region(db, region_id=region_id, region_data=region.model_dump(exclude_unset=True))
                if not db_region:
                    self.handle_not_found(region_id, "Region")
                return db_region
            except IntegrityError as e:
                self.handle_integrity_error(e)

        @self.router.delete("/{region_id}")
        def delete_region(region_id: int, db: Session = Depends(get_db)):
            db_region = self.crud.delete_region(db, region_id=region_id)
            if not db_region:
                self.handle_not_found(region_id, "Region")
            return {"message": "Region deleted successfully"} 