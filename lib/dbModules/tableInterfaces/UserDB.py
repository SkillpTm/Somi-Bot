from lib.dbModules.PostgresDB import PostgresDB



class UserDB():
    """Abstraction layer to interact with the user table."""

    def __init__(self, database: PostgresDB, user_id: int) -> None:
        self.database = database
        self.user_id = user_id

    ####################################################################################################

    async def _get(self, select_columns: list[str]) -> str:
        """get selected column value from the user"""

        return await self.database.fetch_val(
            query_name = "select_where",
            table_name = "user",
            select_columns = select_columns,
            columns = ["user_id"],
            values = [self.user_id]
        )

    ####################################################################################################

    async def _set(self, set_columns: list[str], set_values: list[str]) -> None:
        """set the column values for the user"""

        await self.database.execute(
            query_name = "update_rows_where",
            table_name = "user",
            columns = ["user_id"],
            values = [self.user_id],
            set_columns = set_columns,
            set_values = set_values
        )

    ####################################################################################################

    async def last_fm_get(self) -> str:
        """get the lastfm username from the db"""

        return await self._get(["last_fm_username"])

    ####################################################################################################

    async def last_fm_set(self, last_fm_username: str) -> None:
        """adds the lastfm username to the user in the db"""

        await self._set(["last_fm_username"], [last_fm_username])

    ####################################################################################################

    async def last_fm_reset(self) -> bool:
        """deletes the lastfm username from the user in the db"""

        if not await self.last_fm_get():
            return False

        await self.last_fm_set("")
        return True

    ####################################################################################################

    async def weather_get(self) -> str:
        """get the user's weather location from the db"""

        return await self._get(["weather_location"])

    ####################################################################################################

    async def weather_set(self, weather_location: str) -> None:
        """adds the weather location to the user in the db"""

        self._set(["weather_location"], [weather_location])