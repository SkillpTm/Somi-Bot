from lib.database.DataAccess import DataAccessMixin, Table



class Reminder(DataAccessMixin):
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
    def make_primary_key(key: int | str | None) -> dict[Table, int | str | None]:
        """creates a primary key dict from the primary key value"""

        return {Reminder.ID: key}