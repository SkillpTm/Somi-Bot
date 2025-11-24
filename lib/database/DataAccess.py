import abc
import enum
import typing

from lib.database.Database import Database
from lib.database.Query import Order, Query

T = typing.TypeVar('T')



class Table(enum.Enum):

    @staticmethod
    @abc.abstractmethod
    def get_table() -> str:
        """returns the table name"""


    @staticmethod
    @abc.abstractmethod
    def make_primary_key(key: int | str | None) -> dict["Table", int | str | None]:
        """creates a primary key dict from the primary key value"""


class DataAccessMixin(Table):

    async def add(self: Table, data: dict[Table, int | str | None]) -> bool:
        """adds a new entry into the table"""

        return await Database().execute(
            self.get_table(),
            Query.INSERT,
            data = {key.value: value for key, value in data.items()}
        )


    async def add_unique(
        self: Table,
        where: dict[Table, int | str | None] | int | str | None,
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


    async def delete(self: Table, where: dict[Table, int | str | None] | int | str | None, limit: int = 1) -> bool:
        """deletes an entry from the table"""

        if not isinstance(where, dict):
            where = self.make_primary_key(where)

        return await Database().execute(
            self.get_table(),
            Query.DELETE,
            where = {key.value: value for key, value in where.items()},
            limit = limit
        )


    async def get(self: Table, where: dict[Table, int | str | None] | int | str | None) -> int | str | None:
        """gets a singular value from the table"""

        if not isinstance(where, dict):
            where = self.make_primary_key(where)

        return await Database().fetch_val(
            self.get_table(),
            Query.SELECT,
            select = self.value,
            where = {key.value: value for key, value in where.items()}
        )


    async def get_entry(self: Table, where: dict[Table, int | str | None] | int | str | None) -> dict[str, str | int | None]:
        """gets an entire entry from the table"""

        if not isinstance(where, dict):
            where = self.make_primary_key(where)

        return await Database().fetch_row(
            self.get_table(),
            Query.SELECT,
            where = {key.value: value for key, value in where.items()}
        )


    async def get_multiple(
        self: "Table | DataAccessMixin",
        select: list[Table] = [],
        where: dict[Table, int | str | None] | int | str | None = {},
        order_by: Table = None, #type: ignore
        order: Order = Order.NONE,
        limit: int = 1_000_000
    ) -> typing.AsyncIterator[dict[str, int | str | None]]:
        """gets multiple entries from the table"""

        if typing.cast(Table, self).value:
            select = [typing.cast(Table, self)]

        if not isinstance(where, dict):
            where = typing.cast(Table, self).make_primary_key(where)

        async for entry in Database().fetch_many(
            typing.cast(Table, self).get_table(),
            Query.SELECT,
            select = [column.value for column in select] or ["*"],
            where = {key.value: value for key, value in where.items()} or {"1": 1},
            order_by = order_by.value if order_by else "",
            order = order,
            limit = limit
        ):
            yield entry


    async def get_all(
        self: "Table | DataAccessMixin",
        select: list[Table] = [],
        where: dict[Table, int | str | None] | int | str | None = {},
        order_by: Table = None, #type: ignore
        order: Order = Order.NONE,
        limit: int = 1_000_000
    ) -> list[dict[str, int | str | None]] | list[int | str | None]:
        """the same as get_multiple, but returns all results at once as a list. If only one column is selected, it returns a list of values"""

        output = []

        async for entry in typing.cast(DataAccessMixin, self).get_multiple(
            select = select,
            where = where,
            order_by = order_by,
            order = order,
            limit = limit
        ):
            if len(entry) == 1:
                output = typing.cast(list[int | str | None], output)
                output.append(list(entry.values())[0])
                continue

            output = typing.cast(list[dict[str, int | str | None]], output)
            output.append(entry)

        return output


    async def set(self: Table, where: dict[Table, int | str | None] | int | str | None, data: dict[Table, int | str | None] | int | str | None) -> bool:
        """sets a singular value in the table"""

        if not isinstance(data, dict):
            data = {self: data}

        if not isinstance(where, dict):
            where = self.make_primary_key(where)

        return await Database().execute(
            self.get_table(),
            Query.UPDATE,
            data = {key.value: value for key, value in data.items()},
            where = {key.value: value for key, value in where.items()}
        )

    def retrieve(self: Table, entry: dict[str, T]) -> T:
        """retrieves the value from a result dict"""

        return entry[self.value]