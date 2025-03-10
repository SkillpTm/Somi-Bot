from lib.db_modules.CustomCommandDB import CustomCommandDB
from lib.db_modules.FeedbackDB import FeedbackDB
from lib.db_modules.HiddenChannelDB import HiddenChannelDB
from lib.db_modules.KeywordDB import KeywordDB
from lib.db_modules.LevelDB import LevelDB
from lib.db_modules.LevelIgnoreChannelDB import LevelIgnoreChannelDB
from lib.db_modules.LevelRoleDB import LevelRoleDB
from lib.db_modules.PostgresDB import PostgresDB
from lib.db_modules.ReminderDB import ReminderDB
from lib.db_modules.ServerDB import ServerDB
from lib.db_modules.StatisticDB import StatisticDB
from lib.db_modules.TelemetryDB import TelemetryDB
from lib.db_modules.UserDB import UserDB



class DBHandler():
    """
    This class is a router to be used as an abstraction layer to interact with the database tables.

    On init inserts the provided server into the "server" table and the user into the "user" table, if not already present.
    """


    async def __init__(
        self,
        database: PostgresDB,
        server_id: int = 0,
        user_id: int = 0
    ):
        self.database = database
        self.server_id = server_id
        self.user_id = user_id

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

    def custom_command(self):
        return CustomCommandDB(self.database, self.server_id)

    def feedback(self):
        return FeedbackDB(self.database, self.server_id, self.user_id)

    def hidden_channel(self):
        return HiddenChannelDB(self.database, self.user_id)

    def keyword(self):
        return KeywordDB(self.database, self.server_id, self.user_id)

    def level(self):
        return LevelDB(self.database, self.server_id, self.user_id)

    def level_ignore_channel(self):
        return LevelIgnoreChannelDB(self.database, self.user_id)

    def level_role(self):
        return LevelRoleDB(self.database, self.user_id)

    def reminder(self):
        return ReminderDB(self.database, self.user_id)

    def server(self):
        return ServerDB(self.database, self.server_id)

    def statistic(self):
        return StatisticDB(self.database, self.server_id, self.user_id)

    def telemetry(self):
        return TelemetryDB(self.database)

    def user(self):
        return UserDB(self.database, self.user_id)