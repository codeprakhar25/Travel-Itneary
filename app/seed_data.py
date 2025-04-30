from sqlalchemy.orm import Session
from . import models, crud
from datetime import datetime

def seed_database(db: Session):
    phuket = crud.create_region(db, {
        "name": "Phuket",
        "description": "Thailand's largest island, known for its stunning beaches, vibrant nightlife, and rich cultural heritage."
    })
    
    krabi = crud.create_region(db, {
        "name": "Krabi",
        "description": "A province in southern Thailand known for its dramatic limestone cliffs, pristine beaches, and world-class rock climbing."
    })

    phuket_hotels = [
        {
            "name": "The Nai Harn",
            "location": "Nai Harn Beach",
            "rating": 4.8,
            "price_per_night": 350.0,
            "region_id": phuket.id
        },
        {
            "name": "Trisara",
            "location": "Phang Nga Bay",
            "rating": 4.9,
            "price_per_night": 800.0,
            "region_id": phuket.id
        },
        {
            "name": "The Slate",
            "location": "Nai Yang Beach",
            "rating": 4.7,
            "price_per_night": 250.0,
            "region_id": phuket.id
        },
        {
            "name": "Keemala",
            "location": "Kamala",
            "rating": 4.8,
            "price_per_night": 600.0,
            "region_id": phuket.id
        }
    ]

    krabi_hotels = [
        {
            "name": "Rayavadee",
            "location": "Railay Beach",
            "rating": 4.9,
            "price_per_night": 700.0,
            "region_id": krabi.id
        },
        {
            "name": "Phulay Bay, A Ritz-Carlton Reserve",
            "location": "Tubkaek Beach",
            "rating": 4.9,
            "price_per_night": 900.0,
            "region_id": krabi.id
        },
        {
            "name": "Centara Grand Beach Resort & Villas",
            "location": "Klong Muang Beach",
            "rating": 4.7,
            "price_per_night": 300.0,
            "region_id": krabi.id
        },
        {
            "name": "Dusit Thani Krabi Beach Resort",
            "location": "Klong Muang Beach",
            "rating": 4.6,
            "price_per_night": 280.0,
            "region_id": krabi.id
        }
    ]

    hotels = []
    for hotel_data in phuket_hotels + krabi_hotels:
        hotel = crud.create_hotel(db, hotel_data)
        hotels.append(hotel)

    activities = [
        {
            "name": "Phi Phi Islands Tour",
            "description": "Full-day boat tour to the famous Phi Phi Islands, including snorkeling and beach visits",
            "duration_hours": 8.0,
            "price": 80.0
        },
        {
            "name": "James Bond Island Tour",
            "description": "Boat tour to the iconic limestone karsts featured in 'The Man with the Golden Gun'",
            "duration_hours": 6.0,
            "price": 60.0
        },
        {
            "name": "Old Phuket Town Walking Tour",
            "description": "Explore the historic Sino-Portuguese architecture and local markets",
            "duration_hours": 3.0,
            "price": 40.0
        },
        {
            "name": "Railay Beach Rock Climbing",
            "description": "Half-day rock climbing session with professional instructors",
            "duration_hours": 4.0,
            "price": 70.0
        },
        {
            "name": "Hong Islands Kayaking",
            "description": "Kayaking tour through the stunning lagoons and caves of Hong Islands",
            "duration_hours": 5.0,
            "price": 65.0
        }
    ]

    created_activities = []
    for activity_data in activities:
        activity = crud.create_activity(db, activity_data)
        created_activities.append(activity)

    transfers = [
        {
            "from_location": "Phuket Airport",
            "to_location": "Nai Harn Beach",
            "mode": "Private Car",
            "duration_minutes": 60,
            "price": 40.0
        },
        {
            "from_location": "Krabi Airport",
            "to_location": "Railay Beach",
            "mode": "Boat Transfer",
            "duration_minutes": 45,
            "price": 30.0
        },
        {
            "from_location": "Phuket Town",
            "to_location": "Patong Beach",
            "mode": "Tuk-tuk",
            "duration_minutes": 30,
            "price": 20.0
        }
    ]

    created_transfers = []
    for transfer_data in transfers:
        transfer = crud.create_transfer(db, transfer_data)
        created_transfers.append(transfer)

    itineraries = []
    
    itinerary_2n = crud.create_itinerary(db, {
        "title": "Phuket Beach Escape",
        "description": "A short but sweet beach getaway in Phuket",
        "duration_nights": 2,
        "region_id": phuket.id
    })
    
    day1 = crud.create_day(db, {
        "itinerary_id": itinerary_2n.id,
        "hotel_id": hotels[0].id,
        "day_number": 1
    })
    crud.add_activity_to_day(db, day1.id, created_activities[0].id)
    
    day2 = crud.create_day(db, {
        "itinerary_id": itinerary_2n.id,
        "hotel_id": hotels[0].id,
        "day_number": 2
    })
    crud.add_activity_to_day(db, day2.id, created_activities[2].id)

    itinerary_4n = crud.create_itinerary(db, {
        "title": "Phuket & Krabi Explorer",
        "description": "Explore the best of both Phuket and Krabi",
        "duration_nights": 4,
        "region_id": phuket.id
    })
    
    for i in range(4):
        day = crud.create_day(db, {
            "itinerary_id": itinerary_4n.id,
            "hotel_id": hotels[i % 2].id,
            "day_number": i + 1
        })
        if i == 0:
            crud.add_activity_to_day(db, day.id, created_activities[0].id)
        elif i == 2:
            crud.add_activity_to_day(db, day.id, created_activities[3].id)

    itinerary_6n = crud.create_itinerary(db, {
        "title": "Ultimate Andaman Experience",
        "description": "Comprehensive tour of Phuket and Krabi's highlights",
        "duration_nights": 6,
        "region_id": phuket.id
    })
    
    for i in range(6):
        day = crud.create_day(db, {
            "itinerary_id": itinerary_6n.id,
            "hotel_id": hotels[i % 4].id,
            "day_number": i + 1
        })
        if i == 0:
            crud.add_activity_to_day(db, day.id, created_activities[0].id)
        elif i == 2:
            crud.add_activity_to_day(db, day.id, created_activities[1].id)
        elif i == 4:
            crud.add_activity_to_day(db, day.id, created_activities[3].id)

    itinerary_8n = crud.create_itinerary(db, {
        "title": "Grand Andaman Tour",
        "description": "The ultimate Andaman experience covering all major attractions",
        "duration_nights": 8,
        "region_id": phuket.id
    })
    
    for i in range(8):
        day = crud.create_day(db, {
            "itinerary_id": itinerary_8n.id,
            "hotel_id": hotels[i % 4].id,
            "day_number": i + 1
        })
        if i == 0:
            crud.add_activity_to_day(db, day.id, created_activities[0].id)
        elif i == 2:
            crud.add_activity_to_day(db, day.id, created_activities[1].id)
        elif i == 4:
            crud.add_activity_to_day(db, day.id, created_activities[2].id)
        elif i == 6:
            crud.add_activity_to_day(db, day.id, created_activities[3].id)

    db.commit()
    return {
        "regions": [phuket, krabi],
        "hotels": hotels,
        "activities": created_activities,
        "transfers": created_transfers,
        "itineraries": [itinerary_2n, itinerary_4n, itinerary_6n, itinerary_8n]
    } 