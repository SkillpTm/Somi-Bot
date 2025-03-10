from lib.dbModules.PostgresDB import PostgresDB



class UserDB():
    """Abstraction layer to interact with the user table."""

    async def __init__(self, database: PostgresDB, user_id: int) -> None:
        self.database = database
        self.user_id = user_id

    ####################################################################################################

    async def last_fm_set(self, last_fm_username: str) -> None:
        """adds the lastfm username to the user in the db"""

        await self.database.execute(
            query_name = "update_rows_where",
            table_name = "user",
            columns = ["user_id"],
            values = [str(self.user_id)],
            set_columns = ["last_fm_username"],
            set_values = [last_fm_username]
        )

    ####################################################################################################

    async def last_fm_reset(self) -> None:
        """deletes the lastfm username from the user in the db"""

        return await self.last_fm_set("")
    
    ####################################################################################################

    async def last_fm_get(self) -> str:
        """get the lastfm username from the db"""

        return await self.database.fetch_val(
            query_name = "select_where",
            table_name = "user",
            select_columns=["last_fm_username"],
            columns = ["user_id"],
            values = [str(self.user_id)]
        )
    
    ####################################################################################################

    async def weather_set(self, weather_location: str) -> None:
        """adds the weasther location to the user in the db"""

        await self.database.execute(
            query_name = "update_rows_where",
            table_name = "user",
            columns = ["user_id"],
            values = [str(self.user_id)],
            set_columns = ["weather_location"],
            set_values = [weather_location]
        )

    ####################################################################################################

    async def weather_get(self) -> str:
        """get the user's weather location from the db"""

        return await self.database.fetch_val(
            query_name = "select_where",
            table_name = "user",
            select_columns=["weather_location"],
            columns = ["user_id"],
            values = [str(self.user_id)]
        )