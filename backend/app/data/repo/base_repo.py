from typing import Any, Callable, Dict, List

import asyncpg
from app.data.db_config import DatabaseConfig


class BaseRepo:
    def __init__(self, db_config: DatabaseConfig):
        """Initialize the BaseRepo with a DSN."""
        self.db_config = db_config
        self.initialized = False

    async def initialize(self):
        """Initialize the database connection pool on the first call."""
        if not self.initialized:
            await self.db_config.connect()
            self.initialized = True

    async def fetch_one(self, query: str, *args: Any) -> Dict:
        """Fetch a single record from the database."""
        await self.initialize()
        pool = await self.db_config.get_pool()
        async with pool.acquire() as connection:
            result = await connection.fetchrow(query, *args)
            return dict(result) if result else None

    async def fetch_all(self, query: str, *args: Any) -> List[Dict]:
        """Fetch multiple records from the database."""
        await self.initialize()
        pool = await self.db_config.get_pool()
        async with pool.acquire() as connection:
            results = await connection.fetch(query, *args)
            return [dict(row) for row in results]

    async def execute(self, query: str, *args: Any) -> None:
        """Execute a query without returning results."""
        await self.initialize()
        pool = await self.db_config.get_pool()
        async with pool.acquire() as connection:
            await connection.execute(query, *args)

    async def execute_and_return(self, query: str, *args: Any) -> Dict:
        """Execute a query and return a single result."""
        await self.initialize()
        pool = await self.db_config.get_pool()
        async with pool.acquire() as connection:
            result = await connection.fetchrow(query, *args)
            return dict(result) if result else None

    async def execute_transaction(
        self, operations: Callable[[asyncpg.Connection], Any]
    ) -> Any:
        """
        Execute a set of database operations within a single transaction.

        :param operations: A callable that takes an asyncpg.Connection and executes queries.
        :return: The result of the operation function if applicable.
        """
        await self.initialize()
        pool = await self.db_config.get_pool()
        async with pool.acquire() as connection:
            async with connection.transaction():
                return await operations(connection)
