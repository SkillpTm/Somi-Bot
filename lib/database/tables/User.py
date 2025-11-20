from lib.database.DataAccess import DataAccessMixin, Table



class User(DataAccessMixin):
    ID = "id"
    LASTFM = "last_fm_username"
    WEATHER = "weather_location"
    TIMEZONE = "timezone"

    _ = ""

    @staticmethod
    def get_table() -> str:
        """returns the table name"""

        return "user"


    @staticmethod
    def make_primary_key(key: int | str | None) -> dict[Table, int | str | None]:
        """creates a primary key dict from the primary key value"""

        return {User.ID: key}