from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from database import db
from routers import items, stations, planets, item_types
import os
from dotenv import load_dotenv

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown events"""
    database_url = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/galactic_inventory"
    )
    await db.connect(database_url)
    yield
    await db.disconnect()


app = FastAPI(
    title="Galactic Inventory API",
    description="API for managing galactic inventory across stations and planets",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(items.router)
app.include_router(item_types.router)
app.include_router(stations.router)
app.include_router(planets.router)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Galactic Inventory API",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        pool = db.get_pool()
        async with pool.acquire() as conn:
            await conn.fetchval("SELECT 1")
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}
