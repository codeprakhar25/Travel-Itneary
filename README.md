# Travel Itinerary API

A FastAPI-based travel itinerary management system that provides recommendations for Phuket and Krabi regions in Thailand.

## Features

- RESTful API endpoints for managing travel itineraries
- Day-wise hotel accommodations, transfers, and activities
- Multi-Channel Platform (MCP) integration for recommendations
- PostgreSQL database with SQLAlchemy ORM
- Proper validation and documentation

## Local Development Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/travel-itinerary.git
cd travel-itinerary
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your local database credentials
```

5. Run the application:
```bash
uvicorn app.main:app --reload
```

## Database Setup

1. Create PostgreSQL database:
```bash
createdb travel_itinerary
```

2. Run database migrations:
```bash
alembic upgrade head
```

3. Seed the database:
```bash
python -m app.seed
```

## API Documentation

Once the application is running, access the API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc


## Environment Variables

- `DATABASE_URL`: PostgreSQL connection string
