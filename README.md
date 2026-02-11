# Galactic Inventory API

A FastAPI application for managing galactic inventory across stations and planets using PostgreSQL with asyncpg.
<img width="1009" height="874" alt="Screenshot01" src="https://github.com/user-attachments/assets/4f3fa5a1-6fa3-4ae2-94ee-7b5a98d650e0" />
<img width="1010" height="875" alt="Screenshot02" src="https://github.com/user-attachments/assets/8d4d34cc-384b-45f1-bacb-62ba47361297" />
<img width="1009" height="874" alt="Screenshot03" src="https://github.com/user-attachments/assets/542e54b6-26d6-4510-8d14-86ca9097e99e" />
<img width="1011" height="877" alt="Screenshot04" src="https://github.com/user-attachments/assets/ede0ba2c-48cc-41f1-a9d9-2d972d03ad90" />

## Features

- RESTful API for managing galactic items, stations, and planets
- Web-based UI for easy CRUD operations through the browser
- Inventory management for stations and planets
- Async database operations with asyncpg
- Auto-generated API documentation with Swagger UI and ReDoc
- Health check endpoint

## Prerequisites

- Python 3.8+
- PostgreSQL database running locally
- Database with the galactic inventory schema already created

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure database connection:
```bash
cp .env.example .env
```

3. Edit `.env` and update the `DATABASE_URL` if needed:
```
DATABASE_URL=postgresql://username:password@localhost:5432/galactic_inventory
```

## Running the Application

Start the development server:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- Web UI: http://localhost:8000/static/index.html
- Main API: http://localhost:8000
- Interactive API docs (Swagger UI): http://localhost:8000/docs
- Alternative API docs (ReDoc): http://localhost:8000/redoc
- Health check: http://localhost:8000/health

## Web UI

The application includes a user-friendly web interface for managing your galactic inventory:

1. Open http://localhost:8000/static/index.html in your browser
2. Use the tabs to switch between Items, Stations, and Planets
3. Create new entries using the forms at the top
4. View all entries in cards below the form
5. Use the Update and Delete buttons on each card to modify entries
6. For stations, click "Manage Inventory" to add/remove items from the station's inventory

## API Endpoints

### Items

- `GET /items` - List all items
- `GET /items/{item_id}` - Get a specific item
- `POST /items` - Create a new item
- `PUT /items/{item_id}` - Update an item
- `DELETE /items/{item_id}` - Delete an item

### Stations

- `GET /stations` - List all stations
- `GET /stations/{station_id}` - Get a specific station
- `POST /stations` - Create a new station
- `PUT /stations/{station_id}` - Update a station
- `DELETE /stations/{station_id}` - Delete a station
- `GET /stations/{station_id}/inventory` - Get station inventory with item details
- `POST /stations/{station_id}/inventory?item_id={item_id}` - Add item to station inventory
- `DELETE /stations/{station_id}/inventory/{inventory_id}` - Remove item from station inventory

### Planets

- `GET /planets` - List all planets
- `GET /planets/{planet_id}` - Get a specific planet
- `POST /planets` - Create a new planet
- `PUT /planets/{planet_id}` - Update a planet
- `DELETE /planets/{planet_id}` - Delete a planet
- `GET /planets/{planet_id}/inventory` - Get planet inventory
- `POST /planets/{planet_id}/inventory` - Add to planet inventory
- `DELETE /planets/{planet_id}/inventory/{inventory_id}` - Remove from planet inventory

## Example Usage

### Create an item:
```bash
curl -X POST "http://localhost:8000/items" \
  -H "Content-Type: application/json" \
  -d '{"name": "Plasma Rifle", "description": "Advanced energy weapon"}'
```

### Create a station:
```bash
curl -X POST "http://localhost:8000/stations" \
  -H "Content-Type: application/json" \
  -d '{"name": "Deep Space 9", "description": "Federation space station"}'
```

### Add item to station inventory:
```bash
curl -X POST "http://localhost:8000/stations/1/inventory?item_id=1"
```

### View station inventory:
```bash
curl "http://localhost:8000/stations/1/inventory"
```

## Project Structure

```
galactic_inventory/
├── main.py                 # FastAPI application entry point
├── database.py            # Database connection management
├── models.py              # Pydantic models for request/response
├── routers/
│   ├── __init__.py
│   ├── items.py           # Item endpoints
│   ├── stations.py        # Station and station inventory endpoints
│   └── planets.py         # Planet and planet inventory endpoints
├── static/
│   └── index.html         # Web UI for CRUD operations
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
└── README.md             # This file
```

## Notes

- The `galactic_planets_inventory` table in your schema appears to be missing a `galactic_item_id` column. The planet inventory endpoints work with the current schema but have limited functionality compared to station inventory.
- The `galactic_solar_systems` table is defined in your schema but not currently used in this API.
- All database operations use asyncpg connection pooling for optimal performance.
- The API uses FastAPI's automatic validation and documentation generation.

## Development

To run in development mode with auto-reload:
```bash
uvicorn main:app --reload
```

To run in production mode:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```
