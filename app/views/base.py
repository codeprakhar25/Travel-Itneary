from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Type, List, Optional
from sqlalchemy.exc import IntegrityError, DataError
from ..database import get_db

class BaseView:
    def __init__(self, model: Type, crud_module):
        self.model = model
        self.crud = crud_module
        self.router = APIRouter()
        self.setup_routes()

    def handle_integrity_error(self, e: IntegrityError, detail: str = None):
        if "ix_regions_name" in str(e):
            raise HTTPException(status_code=400, detail="Resource with this name already exists")
        if detail:
            raise HTTPException(status_code=400, detail=detail)
        raise HTTPException(status_code=400, detail=str(e))

    def handle_not_found(self, resource_id: int, resource_type: str):
        raise HTTPException(status_code=404, detail=f"{resource_type} with id {resource_id} does not exist") 