from lib.database.DataAccess import DataAccessMixin, Table



class LevelRole(DataAccessMixin):
    ID = "id"
    SERVER = "server"
    LEVEL = "level"

    _ = ""

    @staticmethod
    def get_table() -> str:
        """returns the table name"""

        return "level_role"


    @staticmethod
    def make_primary_key(key: int | str | None) -> dict[Table, int | str | None]:
        """creates a primary key dict from the primary key value"""

        return {LevelRole.ID: key}