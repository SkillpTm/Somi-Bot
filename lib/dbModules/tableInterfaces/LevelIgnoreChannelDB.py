from lib.dbModules.PostgresDB import PostgresDB



class LevelIgnoreChannelDB():
    """Abstraction layer to interact with the level_ignore_channel table."""

    async def __init__(self, database: PostgresDB, server_id: int) -> None:
        self.database = database
        self.server_id = server_id

    ####################################################################################################
        
    async def add(self, channel_id: int) -> bool:
        """checks if this server already has this channel as a level ignore channel, if not adds it to the db"""

        if await self.database.fetch_row(
            query_name = "select_where",
            table_name = "level_ignore_channel",
            select_columns=["*"],
            columns = ["channel_id"],
            values = [str(channel_id)]
        ):
            return False

        await self.database.execute(
            query_name = "insert_row",
            table_name = "level_ignore_channel",
            columns = ["channel_id", "server_id"],
            values = [str(channel_id), str(self.server_id)]
        )

        return True

    ####################################################################################################
        
    async def delete(self, channel_id: int) -> bool:
        """deletes the channel from the table, if present"""

        if not await self.database.fetch_row(
            query_name = "select_where",
            table_name = "level_ignore_channel",
            select_columns=["*"],
            columns = ["channel_id"],
            values = [str(channel_id)]
        ):
            return False

        await self.database.execute(
            query_name = "delete_rows_where",
            table_name = "level_ignore_channel",
            columns = ["channel_id"],
            values = [str(channel_id)]
        )

        return True

    ####################################################################################################
        
    async def get_list(self) -> list[int]:
        """get a list of all level ignore channel ids in this server"""

        output: list[int] = []

        async for channel_row in self.database.fetch_many(
            query_name = "select_where",
            table_name = "level_ignore_channel",
            select_columns = ["channel_id"],
            columns = ["server_id"],
            values = [str(self.server_id)]
        ):
            output.append(int(channel_row[0]))

        return output