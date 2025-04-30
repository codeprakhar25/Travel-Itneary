from sqlite3 import IntegrityError
from fastapi import Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from .base import BaseView
from .. import schemas, crud
from ..database import get_db

class TransferView(BaseView):
    def setup_routes(self):
        @self.router.post("/", response_model=schemas.Transfer)
        def create_transfer(transfer: schemas.TransferCreate, db: Session = Depends(get_db)):
            try:
                return self.crud.create_transfer(db=db, transfer_data=transfer.model_dump())
            except IntegrityError as e:
                self.handle_integrity_error(e)

        @self.router.get("/", response_model=List[schemas.Transfer])
        def read_transfers(
            skip: int = Query(0, ge=0),
            limit: int = Query(100, ge=1, le=100),
            from_location: Optional[str] = None,
            to_location: Optional[str] = None,
            max_duration: Optional[int] = None,
            max_price: Optional[float] = None,
            db: Session = Depends(get_db)
        ):
            return self.crud.get_transfers(
                db,
                skip=skip,
                limit=limit,
                from_location=from_location,
                to_location=to_location,
                max_duration=max_duration,
                max_price=max_price
            )

        @self.router.get("/{transfer_id}", response_model=schemas.Transfer)
        def read_transfer(transfer_id: int, db: Session = Depends(get_db)):
            db_transfer = self.crud.get_transfer(db, transfer_id=transfer_id)
            if not db_transfer:
                self.handle_not_found(transfer_id, "Transfer")
            return db_transfer

        @self.router.put("/{transfer_id}", response_model=schemas.Transfer)
        def update_transfer(transfer_id: int, transfer: schemas.TransferUpdate, db: Session = Depends(get_db)):
            try:
                if not self.crud.get_transfer(db, transfer_id=transfer_id):
                    self.handle_not_found(transfer_id, "Transfer")
                return self.crud.update_transfer(db, transfer_id=transfer_id, transfer_data=transfer.model_dump(exclude_unset=True))
            except IntegrityError as e:
                self.handle_integrity_error(e)

        @self.router.delete("/{transfer_id}")
        def delete_transfer(transfer_id: int, db: Session = Depends(get_db)):
            db_transfer = self.crud.delete_transfer(db, transfer_id=transfer_id)
            if not db_transfer:
                self.handle_not_found(transfer_id, "Transfer")
            return {"message": "Transfer deleted successfully"} 