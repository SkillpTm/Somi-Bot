import enum

from lib.database.DataAccess import DataAccessMixin, Table

class Reminder(DataAccessMixin, Table, enum.Enum):
    ID = "id"
    USER = "user"
    TIME = "reminder_time"
    LINK = "link"
    MESSAGE = "message"

    _ = ""

    @staticmethod
    def get_table() -> str:
        """returns the table name"""

        return "reminder"


    @staticmethod
    def make_primary_key(key: int | str) -> dict["Reminder", int | str]:
        """creates a primary key dict from the primary key value"""

        return {Reminder.ID: key}