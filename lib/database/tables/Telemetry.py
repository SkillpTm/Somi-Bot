import enum

from lib.database.DataAccess import DataAccessMixin, Table
from lib.database.Database import Database
from lib.database.Query import Query

class Telemetry(DataAccessMixin, Table, enum.Enum):
    NAME = "event_name"
    AMOUNT = "amount"

    _ = ""

    @staticmethod
    def get_table() -> str:
        """returns the table name"""

        return "telemetry"


    @staticmethod
    def make_primary_key(key: int | str) -> dict["Telemetry", int | str]:
        """creates a primary key dict from the primary key value"""

        return {Telemetry.NAME: key}


    @staticmethod
    async def increment(event: str) -> None:
        """Increments the amount of the telemetry event by 1."""

        return await Database().execute(
            Telemetry.get_table(),
            Query.TELENETRY_INCREMENT,
            data = {
                Telemetry.NAME.value: event,
                Telemetry.AMOUNT.value: 1
            }
        )