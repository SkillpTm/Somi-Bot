import enum

from lib.database.DataAccess import DataAccessMixin, Table

class LevelRole(DataAccessMixin, Table, enum.Enum):
    ID = "id"
    SERVER = "server"
    LEVEL = "level"

    _ = ""

    @staticmethod
    def get_table() -> str:
        """returns the table name"""

        return "level_role"


    @staticmethod
    def make_primary_key(key: int | str) -> dict["LevelRole", int | str]:
        """creates a primary key dict from the primary key value"""

        return {LevelRole.ID: key}