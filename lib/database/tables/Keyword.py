from lib.database.DataAccess import DataAccessMixin, Table



class Keyword(DataAccessMixin):
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
    def make_primary_key(key: int | str | None) -> dict[Table, int | str | None]:
        """creates a primary key dict from the primary key value"""

        return {Keyword.ID: key}