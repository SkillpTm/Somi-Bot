import time
import typing

import aiomysql # type: ignore

from lib.database.Query import Order, Query
from lib.managers import Config, Keychain, Singleton



class Database(metaclass=Singleton):

    def __init__(self) -> None:
        self._pool: aiomysql.Pool | None = None
        self._queries: dict[str, str] = {}
        self._set_queries(Config().QUERIES_PATH)


    async def _set_pool(self, schema_path: str, max_pool_size: int) -> None:
        """sets up the db with the provided schema and sets the pool"""

        self._pool = await aiomysql.create_pool(
            host = Keychain().DB_HOST,
            port = Keychain().DB_PORT,
            user = Keychain().DB_USER,
            password = Keychain().DB_PASSWORD,
            db = Keychain().DB_NAME,
            minsize = 1,
            maxsize = max_pool_size,
            cursorclass = aiomysql.DictCursor
        )

        with open(schema_path, "r", encoding="utf-8") as f:
            schema = f.read()

        con: aiomysql.Connection
        cur: aiomysql.Cursor

        # always execute the schema, if a table already exists, this won't create a new one
        async with self._pool.acquire() as con:
            async with con.cursor() as cur:
                await cur.execute(schema)


    def _set_queries(self, queries_path: str) -> None:
        """sets the queries from the provided .sql file"""

        self._queries: dict[str, str] = {}

        with open(queries_path, "r", encoding="utf-8") as f:
            # split the queries by their names
            query_parts = f.read().split("-- name:")[1:]

        for part in query_parts:
            lines = part.strip().split("\n", 1)
            self._queries[lines[0].strip()] = lines[1].strip()


    async def close(self) -> None:
        """closes all pool connections to the db"""

        self._pool.close()
        await self._pool.wait_closed()
        Singleton.reset(Database)


    async def get_latency(self) -> float:
        """gets the latency of the db in milliseconds"""

        start = time.perf_counter()
        con: aiomysql.Connection

        async with self._pool.acquire() as con:
            await con.ping()

        end = time.perf_counter()

        return round((end-start) * 1000, 2)


    async def execute(
        self,
        table: str,
        query: Query,
        *,
        data: dict[str, int | str | None] = {},
        where: dict[str, int | str | None] = {},
        limit: int = 1
    ) -> bool:
        """executes an SQL query"""

        if not self._pool:
            await self._set_pool(Config().SCHEMA_PATH, Config(). DATABASE_POOL_MAX_SIZE)

        formated_query = query.formated(
            self._queries,
            table,
            data = data,
            where = where,
            limit = limit,
        )

        con: aiomysql.Connection
        cur: aiomysql.Cursor

        async with self._pool.acquire() as con:
            async with con.cursor() as cur:
                try:
                    await con.begin()
                    await cur.execute(formated_query, (*data.values(), *where.values()))

                    if cur.rowcount > limit:
                        await con.rollback()
                        return False

                    await con.commit()

                    if cur.rowcount:
                        return True

                except aiomysql.Error:
                    await con.rollback()
                    return False

        return False


    async def fetch_val(
        self,
        table: str,
        query: Query,
        *,
        select: str,
        where: dict[str, int | str | None]
    ) -> int | str | None:
        """fetches a singular value"""

        if not self._pool:
            await self._set_pool(Config().SCHEMA_PATH, Config(). DATABASE_POOL_MAX_SIZE)

        formated_query = query.formated(
            self._queries,
            table,
            select = [select],
            where = where
        )

        con: aiomysql.Connection
        cur: aiomysql.Cursor

        async with self._pool.acquire() as con:
            async with con.cursor() as cur:
                await cur.execute(formated_query, tuple(where.values()))
                result = (await cur.fetchone() or {}).get(select, None)

            await con.commit()

        return result


    async def fetch_row(
        self,
        table: str,
        query: Query,
        *,
        select: list[str] = ["*"],
        where: dict[str, int | str | None] = {}
    ) -> dict[str, str | int | None] | None:
        """fetches a singular row"""

        if not self._pool:
            await self._set_pool(Config().SCHEMA_PATH, Config(). DATABASE_POOL_MAX_SIZE)

        formated_query = query.formated(
            self._queries,
            table,
            select = select,
            where = where
        )

        con: aiomysql.Connection
        cur: aiomysql.Cursor

        async with self._pool.acquire() as con:
            async with con.cursor() as cur:
                await cur.execute(formated_query, tuple(where.values()))
                result = await cur.fetchone()

            await con.commit()

        return result


    async def fetch_many(
        self,
        table: str,
        query: Query,
        *,
        select: list[str] = ["*"],
        where: dict[str, int | str | None] = {},
        order_by: str = "",
        order: Order = Order.NONE,
        limit: int = 1_000_000
    ) -> typing.AsyncIterator[dict[str, str | int | None]]:
        """fetches many rows"""

        if not self._pool:
            await self._set_pool(Config().SCHEMA_PATH, Config(). DATABASE_POOL_MAX_SIZE)

        formated_query = query.formated(
            self._queries,
            table,
            select = select,
            where = where,
            order_by = order_by,
            order = order,
            limit = limit
        )

        con: aiomysql.Connection
        cur: aiomysql.Cursor
        row: dict[str, str | int | None]

        async with self._pool.acquire() as con:
            async with con.cursor() as cur:
                await cur.execute(formated_query, tuple(where.values()))
                async for row in cur:
                    yield row

            await con.commit()