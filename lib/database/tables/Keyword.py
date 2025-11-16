import enum

from lib.database.DataAccess import DataAccessMixin, Table

class Keyword(DataAccessMixin, Table, enum.Enum):
    ID = "id"
    USER = "user"
    SERVER = "server"
    KEYWORD = "keyword"

    _ = ""

    @staticmethod
    def get_table() -> str:
        """returns the table name"""

        return "keyword"

    @staticmethod
    def make_primary_key(key: int | str) -> dict["Keyword", int | str]:
        """creates a primary key dict from the primary key value"""

        return {Keyword.ID: key}