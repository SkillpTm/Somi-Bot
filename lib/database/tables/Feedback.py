from lib.database.DataAccess import DataAccessMixin, Table



class Feedback(DataAccessMixin):
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
    def make_primary_key(key: int | str | None) -> dict[Table, int | str | None]:
        """creates a primary key dict from the primary key value"""

        return {Feedback.ID: key}