from lib.dbModules.tableInterfaces import CustomCommandDB, FeedbackDB, HiddenChannelDB, KeywordDB, LevelDB, LevelIgnoreChannelDB, LevelRoleDB, ReminderDB, ServerDB, StatisticDB, TelemetryDB, UserDB
from lib.dbModules.PostgresDB import PostgresDB



class DBHandler():
    """
    This class is a router to be used as an abstraction layer to interact with the database tables.

    On init inserts the provided server into the "server" table and the user into the "user" table, if not already present.
    """

    def __init__(
        self,
        database: PostgresDB,
        server_id: int = 0,
        user_id: int = 0
    ):
        self.database = database
        self.server_id = server_id
        self.user_id = user_id

    ####################################################################################################

    async def setup(self) -> None:
        """makes sure the user/server always exists in the db"""

        if self.server_id:
            await self.database.execute(
                query_name = "insert_unique_row",
                table_name = "server",
                conflict_columns = ["server_id"],
                columns = ["server_id"],
                values = [str(self.server_id)]
            )

        if self.user_id:
            await self.database.execute(
                query_name = "insert_unique_row",
                table_name = "user",
                conflict_columns = ["user_id"],
                columns = ["user_id"],
                values = [str(self.user_id)]
            )
    
    ####################################################################################################

    async def custom_command(self) -> CustomCommandDB:
        await self.setup()

        return CustomCommandDB(self.database, self.server_id)

    ####################################################################################################

    async def feedback(self) -> FeedbackDB:
        await self.setup()

        return FeedbackDB(self.database, self.server_id, self.user_id)
    
    ####################################################################################################

    async def hidden_channel(self) -> HiddenChannelDB:
        await self.setup()

        return HiddenChannelDB(self.database, self.user_id)
    
    ####################################################################################################

    async def keyword(self) -> KeywordDB:
        await self.setup()

        return KeywordDB(self.database, self.server_id, self.user_id)
    
    ####################################################################################################

    async def level(self) -> LevelDB:
        await self.setup()

        # only attempt to insert the level when both server and user are provided, because not all functions need to be started by a user
        if self.server_id and self.user_id:
            await self.database.execute(
                query_name = "insert_unique_row",
                table_name = "level",
                conflict_columns = ["server_id", "user_id"],
                columns = ["server_id", "user_id"],
                values = [str(self.server_id), str(self.user_id)]
            )

        return LevelDB(self.database, self.server_id, self.user_id)
    
    ####################################################################################################

    async def level_ignore_channel(self) -> LevelIgnoreChannelDB:
        await self.setup()

        return LevelIgnoreChannelDB(self.database, self.user_id)
    
    ####################################################################################################

    async def level_role(self) -> LevelRoleDB:
        await self.setup()

        return LevelRoleDB(self.database, self.user_id)
    
    ####################################################################################################

    async def reminder(self) -> ReminderDB:
        await self.setup()

        return ReminderDB(self.database, self.user_id)
    
    ####################################################################################################

    async def server(self) -> ServerDB:
        await self.setup()

        return ServerDB(self.database, self.server_id)
    
    ####################################################################################################

    async def statistic(self) -> StatisticDB:
        await self.setup()

        await self.database.execute(
            query_name = "insert_unique_row",
            table_name = "statistic",
            conflict_columns = ["server_id", "user_id"],
            columns = ["server_id", "user_id"],
            values = [str(self.server_id), str(self.user_id)]
        )

        return StatisticDB(self.database, self.server_id, self.user_id)
    
    ####################################################################################################

    async def telemetry(self) -> TelemetryDB:
        await self.setup()

        return TelemetryDB(self.database)
    
    ####################################################################################################

    async def user(self) -> UserDB:
        await self.setup()

        return UserDB(self.database, self.user_id)