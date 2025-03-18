import time

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
        *,
        server_id: int = 0,
        user_id: int = 0
    ):
        self.database = database
        self.server_id = server_id
        self.user_id = user_id

    ####################################################################################################

    async def _setup(self) -> None:
        """makes sure the user/server always exists in the db"""

        if self.server_id:
            await self.database.execute(
                query_name = "insert_unique_row",
                table_name = "server",
                conflict_columns = ["server_id"],
                columns = ["server_id"],
                values = [self.server_id]
            )

        if self.user_id:
            await self.database.execute(
                query_name = "insert_unique_row",
                table_name = '"user"',
                conflict_columns = ["user_id"],
                columns = ["user_id"],
                values = [self.user_id]
            )

    ####################################################################################################

    async def get_latency(self) -> int:
        """returns in ms how long a simple select takes on the db"""

        start = time.time()

        _ = await self.database.fetch_row(
            query_name = "select_where",
            table_name = "server",
            select_columns = ["*"],
            columns = ["1"], # we essentaily say 1=1, so we get anything back
            values = [1]
        )

        end = time.time()

        return int(round((end-start) * 1000))

    ####################################################################################################

    async def clear_data(self) -> None:
        """wrapper to delete all server and/or user data, depening on which was provided"""

        if self.server_id:
            await (await self.server()).audit_log_reset()
            await (await self.hidden_channel()).delete_all()
            await (await self.level_ignore_channel()).delete_all()
            await (await self.level_role()).delete_all()
            await (await self.custom_command()).delete_all()
            await (await self.keyword()).delete_all_server()

        if self.user_id:
            await (await self.keyword()).delete_all_server()

    ####################################################################################################

    async def custom_command(self) -> CustomCommandDB:
        await self._setup()

        return CustomCommandDB(self.database, self.server_id)

    ####################################################################################################

    async def feedback(self) -> FeedbackDB:
        await self._setup()

        return FeedbackDB(self.database, self.server_id, self.user_id)
    
    ####################################################################################################

    async def hidden_channel(self) -> HiddenChannelDB:
        await self._setup()

        return HiddenChannelDB(self.database, self.server_id)
    
    ####################################################################################################

    async def keyword(self) -> KeywordDB:
        await self._setup()

        return KeywordDB(self.database, self.server_id, self.user_id)
    
    ####################################################################################################

    async def level(self) -> LevelDB:
        await self._setup()

        # only attempt to insert the level when both server and user are provided, because not all functions need to be started by a user
        if self.server_id and self.user_id:
            await self.database.execute(
                query_name = "insert_unique_row",
                table_name = "level",
                conflict_columns = ["server_id", "user_id"],
                columns = ["server_id", "user_id"],
                values = [self.server_id, self.user_id]
            )

        return LevelDB(self.database, self.server_id, self.user_id)
    
    ####################################################################################################

    async def level_ignore_channel(self) -> LevelIgnoreChannelDB:
        await self._setup()

        return LevelIgnoreChannelDB(self.database, self.server_id)
    
    ####################################################################################################

    async def level_role(self) -> LevelRoleDB:
        await self._setup()

        return LevelRoleDB(self.database, self.server_id)
    
    ####################################################################################################

    async def reminder(self) -> ReminderDB:
        await self._setup()

        return ReminderDB(self.database, self.user_id)
    
    ####################################################################################################

    async def server(self) -> ServerDB:
        await self._setup()

        return ServerDB(self.database, self.server_id)
    
    ####################################################################################################

    async def statistic(self) -> StatisticDB:
        await self._setup()

        await self.database.execute(
            query_name = "insert_unique_row",
            table_name = "statistic",
            conflict_columns = ["server_id", "user_id"],
            columns = ["server_id", "user_id"],
            values = [self.server_id, self.user_id]
        )

        return StatisticDB(self.database, self.server_id, self.user_id)
    
    ####################################################################################################

    async def telemetry(self) -> TelemetryDB:
        await self._setup()

        return TelemetryDB(self.database)
    
    ####################################################################################################

    async def user(self) -> UserDB:
        await self._setup()

        return UserDB(self.database, self.user_id)