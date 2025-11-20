from lib.database.DataAccess import DataAccessMixin, Table



class CustomCommand(DataAccessMixin):
    ID = "id"
    SERVER = "server"
    NAME = "name"
    TEXT = "text"

    _ = ""

    @staticmethod
    def get_table() -> str:
        """returns the table name"""

        return "custom_command"


    @staticmethod
    def make_primary_key(key: int | str | None) -> dict[Table, int | str | None]:
        """creates a primary key dict from the primary key value"""

        return {CustomCommand.ID: key}