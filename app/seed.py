from .database import SessionLocal
from .seed_data import seed_database

def main():
    db = SessionLocal()
    try:
        print("Seeding database...")
        result = seed_database(db)
        print(f"Created {len(result['regions'])} regions")
        print(f"Created {len(result['hotels'])} hotels")
        print(f"Created {len(result['activities'])} activities")
        print(f"Created {len(result['transfers'])} transfers")
        print(f"Created {len(result['itineraries'])} itineraries")
        print("Database seeding completed successfully!")
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main() 