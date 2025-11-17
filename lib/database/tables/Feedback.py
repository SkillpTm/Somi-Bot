import enum

from lib.database.DataAccess import DataAccessMixin, Table

class Feedback(DataAccessMixin, Table, enum.Enum):
    ID = "id"
    USER = "user"
    SERVER = "server"
    MESSAGE = "message"
    TIME = "created_at"

    _ = ""

    @staticmethod
    def get_table() -> str:
        """returns the table name"""

        return "feedback"


    @staticmethod
    def make_primary_key(key: int | str) -> dict["Feedback", int | str]:
        """creates a primary key dict from the primary key value"""

        return {Feedback.ID: key}