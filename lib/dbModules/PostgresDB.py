import asyncpg
import os



class PostgresDB():

    async def __init__(
        self,
        schema_path: str,
        queries_path: str,
        max_pool_size: int
    ) -> None:
        self._pool = await self._setup(schema_path, max_pool_size)
        self._queries = self._setup_queries(queries_path)

    ####################################################################################################

    @staticmethod
    async def _setup(schema_path: str, max_pool_size: int) -> asyncpg.Pool:
        """sets up the db with the provided schema and returns the pool"""

        DB_HOST: str = os.getenv("DB_HOST")
        DB_PORT: str = os.getenv("DB_PORT")
        DB_USER: str = os.getenv("DB_USER")
        DB_PASSWORD: str = os.getenv("DB_PASSWORD")
        DB_NAME: str = os.getenv("DB_NAME")

        # login to default db to check if our db exists
        conn: asyncpg.connection.Connection = await asyncpg.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database="postgres"
        )

        # create the DB, if it doesn't already exist
        if not await conn.fetchval("SELECT 1 FROM pg_database WHERE datname = $1", DB_NAME):
            await conn.execute(f"CREATE DATABASE {DB_NAME}")

        await conn.close()

        pool = await asyncpg.create_pool(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            min_size=1,
            max_size=max_pool_size
        )

        with open(schema_path, 'r') as f:
            schema = f.read()

        # always execute the schema, if a table already exists, this won't create a new one
        async with pool.acquire() as conn:
            async with conn.transaction():
                await conn.execute(schema)

        return pool

    ####################################################################################################

    @staticmethod
    def _setup_queries(queries_path: str) -> dict[str, str]:
        """gets the queries from the provided .sql file"""

        queries: dict[str, str] = {}

        with open(queries_path, 'r') as f:
            # split the queries by their names
            query_parts = f.read().split('-- name:')[1:]
        
        for part in query_parts:
            lines = part.strip().split('\n', 1)
            queries[lines[0].strip()] = lines[1].strip()

        return queries

    ####################################################################################################

    @staticmethod
    def _sanitize(values: list[str]) -> list[str]:
        """sanitizes any input values or columns for sql"""

        for index, element in enumerate(values):
            values[index] = str(element).replace('"', '＂').replace("'", "‘")

        return values

    ####################################################################################################

    @staticmethod
    def _desanitize(values: list[str]) -> list[str]:
        """desanitizes any input values or columns from our db"""

        for index, element in enumerate(values):
            values[index] = str(element).replace('＂', '"').replace("‘", "'")

        return values

    ####################################################################################################

    def _get_query(
        self,
        *,
        query_name: str,
        table_name: str = "",
        select_columns: list[str] = [],
        conflict_columns: list[str] = [],
        limit: int = 0,
        columns: list[str] = [],
        values: list[str] = [],
        set_columns: list[str] = [],
        set_values: list[str] = []
    ) -> str:
        """"""

        query = self._queries[query_name]

        if table_name:
            query.replace(":table_name", self._sanitize([table_name])[0])

        if select_columns:
            query.replace(":select_columns", ", ".join(self._sanitize(select_columns)))

        if conflict_columns:
            query.replace(":conflict_columns", ", ".join(self._sanitize(conflict_columns)))

        if limit:
            query.replace(":limit_value", ", ".join(self._sanitize(str(limit))))

        if columns:
            query.replace(":column_names", ", ".join(self._sanitize(columns)))

        # if there are values add the $num placeholders for asyncpg to resolve later
        if values:
            query.replace(":placeholder_values", ", ".join(f"${i+1}" for i in range(len(set_values), len(set_values) + len(values))))

        if set_columns:
            query.replace(":set_column_names", ", ".join(self._sanitize(set_columns)))

        # if there are values add the $num placeholders for asyncpg to resolve later
        if set_values:
            query.replace(":placeholder_values", ", ".join(f"${i+1}" for i in range(len(set_values))))

        return query

    ####################################################################################################

    async def execute(
        self,
        *,
        query_name: str,
        table_name: str = "",
        conflict_columns: list[str] = [],
        columns: list[str] = [],
        values: list[str] = [],
        set_columns: list[str] = [],
        set_values: list[str] = []
    ) -> None:
        """"""

        query = self._get_query(
            query_name = query_name,
            table_name = table_name,
            conflict_columns = conflict_columns,
            columns = columns,
            values = values,
            set_columns = set_columns,
            set_values=set_values
        )

        async with self._pool.acquire() as conn:
            await conn.execute(query, *self._sanitize(set_values), *self._sanitize(values))

    ####################################################################################################

    async def fetch_val(
        self,
        *,
        query_name: str,
        table_name: str = "",
        select_columns: list[str] = [],
        columns: list[str] = [],
        values: list[str] = []
    ) -> str | int:
        """"""

        query = self._get_query(
            query_name = query_name,
            table_name = table_name,
            select_columns = select_columns,
            columns = columns,
            values = values
        )

        async with self._pool.acquire() as conn:
            result: str | int | None = await conn.fetchval(query, *self._sanitize(values))

        if type(result) == str:
            result = self._desanitize([result])[0]

        # ensure we never return null
        if not result:
            return ""

        return result
    
    ####################################################################################################

    async def fetch_row(
        self,
        *,
        query_name: str,
        table_name: str = "",
        select_columns: list[str] = [],
        limit: int = 0,
        columns: list[str] = [],
        values: list[str] = []
    ) -> list[str | int]:
        """"""

        query = self._get_query(
            query_name = query_name,
            table_name = table_name,
            select_columns = select_columns,
            limit = limit,
            columns = columns,
            values = values
        )

        async with self._pool.acquire() as conn:
            result: asyncpg.Record | None = await conn.fetchrow(query, *self._sanitize(values))

        output: list[str | int] = []

        if not result:
            return output

        for value in result.values():
            if type(value) == str:
                value = self._desanitize([value])[0]

            # ensure we never return null
            if not value:
                value = ""

            output.append(value)

        return output
    
    ####################################################################################################

    async def fetch_many(
        self,
        *,
        query_name: str,
        table_name: str = "",
        select_columns: list[str] = [],
        limit: int = 0,
        columns: list[str] = [],
        values: list[str] = []
    ) -> list[list[str | int]]:
        """"""

        query = self._get_query(
            query_name = query_name,
            table_name = table_name,
            select_columns = select_columns,
            limit=limit,
            columns = columns,
            values = values
        )

        async with self._pool.acquire() as conn:
            results: list[asyncpg.Record] = await conn.fetchmany(query, *self._sanitize(values))

        output: list[list[str | int]] = []

        for index, result in enumerate(results):
            for value in result.values():
                if type(value) == str:
                    value = self._desanitize([value])[0]

                # ensure we never return null
                if not value:
                    value = ""

                output[index].append(value)

        return output