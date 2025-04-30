from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models
from .database import engine
from .views import RegionView, HotelView, ItineraryView, ActivityView, DayView, TransferView
from .mcp_server import router as mcp_router
from . import crud, schemas
import json
from decimal import Decimal

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Travel Itinerary API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

app.json_encoder = DecimalEncoder

region_view = RegionView(schemas.Region, crud)
hotel_view = HotelView(schemas.Hotel, crud)
itinerary_view = ItineraryView(schemas.Itinerary, crud)
activity_view = ActivityView(schemas.Activity, crud)
day_view = DayView(schemas.Day, crud)
transfer_view = TransferView(schemas.Transfer, crud)

app.include_router(region_view.router, prefix="/regions", tags=["regions"])
app.include_router(hotel_view.router, prefix="/hotels", tags=["hotels"])
app.include_router(itinerary_view.router, prefix="/itineraries", tags=["itineraries"])
app.include_router(activity_view.router, prefix="/activities", tags=["activities"])
app.include_router(day_view.router, prefix="/days", tags=["days"])
app.include_router(transfer_view.router, prefix="/transfers", tags=["transfers"])
app.include_router(mcp_router, tags=["mcp"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Travel Itinerary API"}