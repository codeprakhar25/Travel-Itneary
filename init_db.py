import time
import os
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from app.database import Base, engine
from app import models
from app.seed_data import seed_database
from app.database import SessionLocal

def wait_for_postgres():
    max_retries = 5
    retry_count = 0
    while retry_count < max_retries:
        try:
            engine = create_engine("postgresql://postgres:postgres@localhost:5432/travel_db")
            engine.connect()
            print("PostgreSQL is ready!")
            return True
        except OperationalError:
            retry_count += 1
            print(f"Waiting for PostgreSQL... Attempt {retry_count}/{max_retries}")
            time.sleep(5)
    return False

def init_database():
    if not wait_for_postgres():
        print("Failed to connect to PostgreSQL. Exiting...")
        return

    print("Creating database tables...")
    try:
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully!")
    except Exception as e:
        print(f"Error creating tables: {e}")
        return
    
    print("Seeding database with initial data...")
    db = SessionLocal()
    try:
        seed_database(db)
        print("Database seeded successfully!")
    except Exception as e:
        print(f"Error seeding database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    init_database() 