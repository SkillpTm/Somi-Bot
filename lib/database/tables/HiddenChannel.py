from lib.database.DataAccess import DataAccessMixin, Table



class HiddenChannel(DataAccessMixin):
    ID = "id"
    SERVER = "server"

    _ = ""

    @staticmethod
    def get_table() -> str:
        """returns the table name"""

        return "hidden_channel"


    @staticmethod
    def make_primary_key(key: int | str | None) -> dict[Table, int | str | None]:
        """creates a primary key dict from the primary key value"""

        return {HiddenChannel.ID: key}