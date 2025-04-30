import uvicorn
from app.database import SessionLocal
from app.seed_data import seed_database
from init_db import init_database

if __name__ == "__main__":
    # Initialize database and seed data
    init_database()
    
    # Run the FastAPI application
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 