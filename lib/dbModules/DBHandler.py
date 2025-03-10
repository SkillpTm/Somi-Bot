from lib.dbModules.tableInterfaces.CustomCommandDB import CustomCommandDB
from lib.dbModules.tableInterfaces.FeedbackDB import FeedbackDB
from lib.dbModules.tableInterfaces.HiddenChannelDB import HiddenChannelDB
from lib.dbModules.tableInterfaces.KeywordDB import KeywordDB
from lib.dbModules.tableInterfaces.LevelDB import LevelDB
from lib.dbModules.tableInterfaces.LevelIgnoreChannelDB import LevelIgnoreChannelDB
from lib.dbModules.tableInterfaces.LevelRoleDB import LevelRoleDB
from lib.dbModules.PostgresDB import PostgresDB
from lib.dbModules.tableInterfaces.ReminderDB import ReminderDB
from lib.dbModules.tableInterfaces.ServerDB import ServerDB
from lib.dbModules.tableInterfaces.StatisticDB import StatisticDB
from lib.dbModules.tableInterfaces.TelemetryDB import TelemetryDB
from lib.dbModules.tableInterfaces.UserDB import UserDB



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