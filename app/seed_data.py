from sqlalchemy.orm import Session
from . import models, crud
from datetime import datetime
from .models import LocationType

def seed_database(db: Session):
    try:
        # Create regions
        phuket = crud.create_region(db, {
            "name": "Phuket",
            "description": "Thailand's largest island, known for its beaches, nightlife, and luxury resorts."
        })
        
        krabi = crud.create_region(db, {
            "name": "Krabi",
            "description": "A province in southern Thailand known for its stunning limestone cliffs and islands."
        })
        
        # Create hotels in Phuket
        phuket_hotels = [
            {
                "name": "The Nai Harn",
                "location": "Nai Harn Beach",
                "location_type": LocationType.BEACH,
                "rating": 4.8,
                "price_per_night": 350.0,
                "region_id": phuket.id
            },
            {
                "name": "Trisara",
                "location": "Phuket",
                "location_type": LocationType.BEACH,
                "rating": 4.9,
                "price_per_night": 800.0,
                "region_id": phuket.id
            },
            {
                "name": "The Slate",
                "location": "Nai Yang Beach",
                "location_type": LocationType.BEACH,
                "rating": 4.7,
                "price_per_night": 250.0,
                "region_id": phuket.id
            },
            {
                "name": "Keemala",
                "location": "Kamala",
                "location_type": LocationType.MOUNTAIN,
                "rating": 4.8,
                "price_per_night": 600.0,
                "region_id": phuket.id
            }
        ]
        
        # Create hotels in Krabi
        krabi_hotels = [
            {
                "name": "Rayavadee",
                "location": "Railay Beach",
                "location_type": LocationType.BEACH,
                "rating": 4.9,
                "price_per_night": 700.0,
                "region_id": krabi.id
            },
            {
                "name": "Phulay Bay",
                "location": "Krabi",
                "location_type": LocationType.BEACH,
                "rating": 4.8,
                "price_per_night": 500.0,
                "region_id": krabi.id
            },
            {
                "name": "Ritz-Carlton Reserve",
                "location": "Phulay Bay",
                "location_type": LocationType.BEACH,
                "rating": 4.9,
                "price_per_night": 900.0,
                "region_id": krabi.id
            },
            {
                "name": "Centara Grand Beach Resort",
                "location": "Klong Muang Beach",
                "location_type": LocationType.BEACH,
                "rating": 4.7,
                "price_per_night": 300.0,
                "region_id": krabi.id
            }
        ]
        
        # Create all hotels
        hotels = []
        for hotel_data in phuket_hotels + krabi_hotels:
            hotel = crud.create_hotel(db, hotel_data)
            hotels.append(hotel)
        
        # Create activities
        activities = [
            {
                "name": "Phi Phi Islands Tour",
                "description": "Full-day boat tour to Phi Phi Islands with snorkeling and lunch",
                "duration_hours": 8.0,
                "price": 100.0
            },
            {
                "name": "James Bond Island Tour",
                "description": "Visit the famous James Bond Island and surrounding limestone caves",
                "duration_hours": 6.0,
                "price": 80.0
            },
            {
                "name": "Elephant Sanctuary Visit",
                "description": "Ethical elephant experience with feeding and bathing",
                "duration_hours": 4.0,
                "price": 120.0
            },
            {
                "name": "Old Town Walking Tour",
                "description": "Explore Phuket's historic old town with local guide",
                "duration_hours": 3.0,
                "price": 50.0
            },
            {
                "name": "Tiger Cave Temple",
                "description": "Visit the famous temple and climb 1,237 steps for panoramic views",
                "duration_hours": 4.0,
                "price": 40.0
            }
        ]
        
        created_activities = []
        for activity_data in activities:
            activity = crud.create_activity(db, activity_data)
            created_activities.append(activity)
        
        # Create transfers
        transfers = [
            {
                "from_location": "Phuket Airport",
                "to_location": "Patong Beach",
                "mode": "PRIVATE_CAR",
                "duration_minutes": 45,
                "price": 50.0
            },
            {
                "from_location": "Krabi Airport",
                "to_location": "Railay Beach",
                "mode": "SPEEDBOAT",
                "duration_minutes": 30,
                "price": 40.0
            },
            {
                "from_location": "Phuket",
                "to_location": "Krabi",
                "mode": "FERRY",
                "duration_minutes": 120,
                "price": 30.0
            }
        ]
        
        created_transfers = []
        for transfer_data in transfers:
            transfer = crud.create_transfer(db, transfer_data)
            created_transfers.append(transfer)
        
        # Create itineraries
        itineraries = [
            {
                "title": "Phuket Weekend Getaway",
                "description": "2-night luxury stay in Phuket",
                "duration_nights": 2,
                "region_id": phuket.id
            },
            {
                "title": "Phuket & Krabi Explorer",
                "description": "4-night adventure in both regions",
                "duration_nights": 4,
                "region_id": phuket.id
            },
            {
                "title": "Southern Thailand Discovery",
                "description": "6-night comprehensive tour",
                "duration_nights": 6,
                "region_id": phuket.id
            },
            {
                "title": "Ultimate Thailand Experience",
                "description": "8-night luxury vacation",
                "duration_nights": 8,
                "region_id": phuket.id
            }
        ]
        
        created_itineraries = []
        for itinerary_data in itineraries:
            itinerary = crud.create_itinerary(db, itinerary_data)
            created_itineraries.append(itinerary)
            
            # Create days for each itinerary
            for day_num in range(1, itinerary_data["duration_nights"] + 1):
                # Select hotel based on day number and region
                if day_num <= 2:
                    hotel = next(h for h in hotels if h.region_id == phuket.id)
                else:
                    hotel = next(h for h in hotels if h.region_id == krabi.id)
                
                day = crud.create_day(db, {
                    "day_number": day_num,
                    "itinerary_id": itinerary.id,
                    "hotel_id": hotel.id
                })
                
                # Add activities to days
                if day_num == 1:
                    crud.create_day_activity(db, {
                        "day_id": day.id,
                        "activity_id": created_activities[0].id
                    })
                elif day_num == 2:
                    crud.create_day_activity(db, {
                        "day_id": day.id,
                        "activity_id": created_activities[1].id
                    })
                
                # Add transfers between regions
                if day_num == 3:
                    crud.create_day_transfer(db, {
                        "day_id": day.id,
                        "transfer_id": created_transfers[2].id
                    })
        
        db.commit()
        return {
            "regions": 2,
            "hotels": len(hotels),
            "activities": len(created_activities),
            "transfers": len(created_transfers),
            "itineraries": len(created_itineraries)
        }
        
    except Exception as e:
        db.rollback()
        raise Exception(f"Error seeding database: {str(e)}") 