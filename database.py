import asyncpg
from typing import Optional


class Database:
    def __init__(self):
        self.pool: Optional[asyncpg.Pool] = None

    async def connect(self, dsn: str):
        """Create database connection pool"""
        self.pool = await asyncpg.create_pool(
            dsn,
            min_size=5,
            max_size=20,
            command_timeout=60
        )

    async def disconnect(self):
        """Close database connection pool"""
        if self.pool:
            await self.pool.close()

    def get_pool(self) -> asyncpg.Pool:
        """Get the database pool"""
        if not self.pool:
            raise RuntimeError("Database pool is not initialized")
        return self.pool


db = Database()
