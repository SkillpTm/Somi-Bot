import abc
from typing import AsyncIterator, Union

from lib.database.Database import Database
from lib.database.Query import Order, Query



class Table():
    # Tables must be an Enum
    name: str
    value: str

    @staticmethod
    @abc.abstractmethod
    def get_table() -> str:
        """returns the table name"""
        pass

    @staticmethod
    @abc.abstractmethod
    def make_primary_key(key: int | str) -> dict["Table", int | str]:
        """creates a primary key dict from the primary key value"""
        pass

class DataAccessMixin():
    async def add(self: Table, data: dict[Table, int | str | None]) -> bool:
        """adds a new entry into the table"""

        return await Database().execute(
            self.get_table(),
            Query.INSERT,
            data = {key.value: value for key, value in data.items()}
        )

    async def add_unique(
        self: Table,
        where: dict[Table, int | str | None] | int | str,
        data: dict[Table, int | str | None]
    ) -> bool:
        """adds a new unique entry into the table"""

        if not isinstance(where, dict):
            where = self.make_primary_key(where)

        return await Database().execute(
            self.get_table(),
            Query.INSERT_UNIQUE,
            data = {key.value: value for key, value in data.items()},
            where = {key.value: value for key, value in where.items()}
        )

    async def delete(self: Table, where: dict[Table, int | str | None] | int | str, limit: int = 1) -> bool:
        """deletes an entry from the table"""

        if not isinstance(where, dict):
            where = self.make_primary_key(where)

        return await Database().execute(
            self.get_table(),
            Query.DELETE,
            where = {key.value: value for key, value in where.items()},
            limit = limit
        )

    async def get(self: Table, where: dict[Table, int | str | None] | int | str) -> int | str | None:
        """gets a singular value from the table"""

        if not isinstance(where, dict):
            where = self.make_primary_key(where)

        return await Database().fetch_val(
            self.get_table(),
            Query.SELECT,
            select = self.value,
            where = {key.value: value for key, value in where.items()}
        )

    async def get_entry(self: Table, where: dict[Table, int | str | None] | int | str) -> dict[str, str | int | None] | None:
        """gets an entire entry from the table"""

        if not isinstance(where, dict):
            where = self.make_primary_key(where)

        return await Database().fetch_row(
            self.get_table(),
            Query.SELECT,
            where = {key.value: value for key, value in where.items()}
        )

    async def get_multiple(
        self: Table,
        select: list[Table] = [],
        where: dict[Table, int | str | None] | int | str = {},
        order_by: Table = None,
        order: Order = Order.NONE,
        limit: int = 1_000_000
    ) -> AsyncIterator[dict[str, str | int | None]]:
        """gets multiple entries from the table"""

        if self.value:
            select = [self]

        if not isinstance(where, dict):
            where = self.make_primary_key(where)

        async for entry in Database().fetch_many(
            self.get_table(),
            Query.SELECT,
            select = [column.value for column in select] or ["*"],
            where = {key.value: value for key, value in where.items()} or {"1": 1},
            order_by = order_by.value if isinstance(order_by, Table) else "",
            order = order,
            limit = limit
        ):
            yield entry

    async def get_all(
        self: Union[Table, "DataAccessMixin"],
        select: list[Table] = [],
        where: dict[Table, int | str | None] | int | str = {},
        order_by: Table = None,
        order: Order = Order.NONE,
        limit: int = 1_000_000
    ) -> list[dict[str, str | int | None]] | list[str | int | None]:
        """the same as get_multiple, but returns all results at once as a list. If only one column is selected, it returns a list of values"""

        output = []
        entry: dict[str, str | int | None]

        async for entry in self.get_multiple(
            select = select,
            where = where,
            order_by = order_by,
            order = order,
            limit = limit
        ):
            if len(entry) == 1:
                output.append(list(entry.values())[0])
                continue

            output.append(entry)

        return output

    async def set(self: Table, where: dict[Table, int | str | None] | int | str, data: dict[Table, int | str | None] | int | str) -> bool:
        """sets a singular value in the table"""

        if not isinstance(data, dict):
            data: dict[Table, int | str | None] = {self: data}

        if not isinstance(where, dict):
            where: dict[Table, int | str | None] = self.make_primary_key(where)

        return await Database().execute(
            self.get_table(),
            Query.UPDATE,
            data = {key.value: value for key, value in where.items()},
            where = {key.value: value for key, value in where.items()}
        )

    def retrieve(self: Table, entry: dict[Table, int | str | None]) -> int | str | None:
        """retrieves the value from a result dict"""

        return entry[self.value]