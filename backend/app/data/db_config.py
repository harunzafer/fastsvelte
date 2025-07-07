import json
import ssl
from typing import Optional
from urllib.parse import urlparse
import logging as log
import asyncpg


class DatabaseConfig:
    def __init__(
        self,
        dsn: str,
        min_size: int = 10,
        max_size: int = 30,
        max_inactive_connection_lifetime: float = 300.0,
    ):
        self._dsn = dsn
        self._pool: Optional[asyncpg.Pool] = None
        self._ssl_context: Optional[ssl.SSLContext] = self._create_ssl_context(dsn)
        self._min_size = min_size
        self._max_size = max_size
        self._max_inactive_connection_lifetime = max_inactive_connection_lifetime

    def _create_ssl_context(self, dsn: str) -> Optional[ssl.SSLContext]:
        """Create an SSL context only if required."""
        parsed_url = urlparse(dsn)
        if parsed_url.hostname in ("localhost", "127.0.0.1"):
            log.info("Disabling SSL for local database connection.")
            return None  # No SSL for local connections

        if "sslmode=disable" in dsn:
            log.info("SSL disabled based on connection string.")
            return None

        # Default: Enforce SSL for remote databases
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = True
        ssl_context.verify_mode = ssl.CERT_REQUIRED
        return ssl_context

    async def _init_connection(self, connection: asyncpg.Connection):
        """Initialize the connection with custom type decoding for JSONB."""
        await connection.set_type_codec(
            "jsonb",
            encoder=lambda v: json.dumps(v),
            decoder=lambda v: json.loads(v),
            schema="pg_catalog",
        )

    async def connect(self):
        """Initialize the database connection pool."""
        if not self._pool:
            self._pool = await asyncpg.create_pool(
                self._dsn,
                ssl=self._ssl_context,
                init=self._init_connection,
                min_size=self._min_size,
                max_size=self._max_size,
                max_inactive_connection_lifetime=self._max_inactive_connection_lifetime,
            )

    async def disconnect(self):
        """Close the database connection pool."""
        if self._pool:
            log.info("Disconnecting from the database...", flush=True)
            await self._pool.close()
            self._pool = None

    async def get_pool(self) -> asyncpg.Pool:
        """Retrieve the database connection pool."""
        if not self._pool:
            raise RuntimeError(
                "Database connection pool is not initialized. Call `connect()` first."
            )
        return self._pool
