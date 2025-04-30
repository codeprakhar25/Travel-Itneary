from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from . import crud, models, schemas
from fastapi import APIRouter, Depends, HTTPException, Query
from .database import get_db, SessionLocal
from mcp.server.fastmcp import FastMCP
import numpy as np
from datetime import datetime

mcp = FastMCP("travel_itinerary")

class ItineraryRecommender:
    def __init__(self, db: Session):
        self.db = db
        self.itineraries = self._load_itineraries()
        self.regions = self._load_regions()
        self.hotels = self._load_hotels()

    def _load_itineraries(self) -> List[models.Itinerary]:
        return self.db.query(models.Itinerary).all()

    def _load_regions(self) -> List[models.Region]:
        return self.db.query(models.Region).all()

    def _load_hotels(self) -> List[models.Hotel]:
        return self.db.query(models.Hotel).all()

    def _calculate_similarity_score(self, target_itinerary: models.Itinerary, 
                                  candidate_itinerary: models.Itinerary) -> float:
        score = 0.0
        
        if target_itinerary.duration_nights == candidate_itinerary.duration_nights:
            score += 0.4
        else:
            diff = abs(target_itinerary.duration_nights - candidate_itinerary.duration_nights)
            score += max(0, 0.4 - (diff * 0.1))

        # Region similarity
        if target_itinerary.region_id == candidate_itinerary.region_id:
            score += 0.3

        # Hotel rating similarity
        target_hotels = [day.hotel for day in target_itinerary.days]
        candidate_hotels = [day.hotel for day in candidate_itinerary.days]
        
        if target_hotels and candidate_hotels:
            avg_target_rating = np.mean([h.rating for h in target_hotels])
            avg_candidate_rating = np.mean([h.rating for h in candidate_hotels])
            rating_diff = abs(avg_target_rating - avg_candidate_rating)
            score += max(0, 0.3 - (rating_diff * 0.1))

        return score

    def recommend_itineraries(self, 
                            duration_nights: int,
                            region_id: Optional[int] = None,
                            min_rating: Optional[float] = None,
                            max_price: Optional[float] = None,
                            limit: int = 5) -> List[Dict]:
        
        target_itinerary = models.Itinerary(
            duration_nights=duration_nights,
            region_id=region_id if region_id else 1
        )

        scored_itineraries = []
        for itinerary in self.itineraries:
            if region_id and itinerary.region_id != region_id:
                continue
                
            if min_rating:
                hotel_ratings = [day.hotel.rating for day in itinerary.days]
                if not hotel_ratings or min(hotel_ratings) < min_rating:
                    continue
                    
            if max_price:
                total_price = sum(day.hotel.price_per_night for day in itinerary.days)
                if total_price > max_price:
                    continue

            score = self._calculate_similarity_score(target_itinerary, itinerary)
            scored_itineraries.append((itinerary, score))

        scored_itineraries.sort(key=lambda x: x[1], reverse=True)
        recommendations = []
        
        for itinerary, score in scored_itineraries[:limit]:
            hotel_ratings = [day.hotel.rating for day in itinerary.days]
            avg_rating = float(np.nanmean(hotel_ratings)) if hotel_ratings else 0.0
            
            recommendations.append({
                "itinerary_id": itinerary.id,
                "title": itinerary.title,
                "duration_nights": itinerary.duration_nights,
                "region": next(r.name for r in self.regions if r.id == itinerary.region_id),
                "hotels": [day.hotel.name for day in itinerary.days],
                "total_price": float(sum(day.hotel.price_per_night for day in itinerary.days)),
                "average_rating": avg_rating,
                "similarity_score": float(score)
            })

        return recommendations

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@mcp.tool()
async def get_recommended_itineraries(duration_nights: int, limit: int = 5) -> List[dict]:
    """
    Get recommended itineraries based on duration in nights.
    
    Args:
        duration_nights: Number of nights for the itinerary (2-8)
        limit: Maximum number of itineraries to return (default: 5)
    
    Returns:
        List of recommended itineraries with details
    """
    if duration_nights < 2 or duration_nights > 8:
        return [{"error": "Duration must be between 2 and 8 nights"}]
    
    db = SessionLocal()
    try:
        recommender = ItineraryRecommender(db)
        recommendations = recommender.recommend_itineraries(
            duration_nights=duration_nights,
            limit=limit
        )
        return recommendations
    finally:
        db.close()

router = APIRouter(prefix="/mcp", tags=["recommendations"])

@router.get("/recommendations/")
async def get_recommendations(
    duration_nights: int = Query(..., ge=2, le=8),
    region_id: Optional[int] = None,
    min_rating: Optional[float] = None,
    max_price: Optional[float] = None,
    limit: int = Query(5, ge=1, le=10),
    db: Session = Depends(get_db)
):
    """
    Get recommended itineraries with optional filters.
    """
    recommender = ItineraryRecommender(db)
    recommendations = recommender.recommend_itineraries(
        duration_nights=duration_nights,
        region_id=region_id,
        min_rating=min_rating,
        max_price=max_price,
        limit=limit
    )
    return {"recommendations": recommendations}

@router.get("/mcp/recommendations/")
async def get_recommendations_through_mcp(
    duration_nights: int = Query(..., ge=2, le=8),
    limit: int = Query(5, ge=1, le=10)
):
    """
    Get recommended itineraries through MCP integration.
    """
    return await get_recommended_itineraries(duration_nights, limit) 
