import math
import operator
import time

from lib.db_modules.PostgresDB import PostgresDB



class LevelDB():
    """
    Abstraction layer to interact with the level table.

    On init inserts the user with the server into the "level" table, if not already present.
    """

    async def __init__(
        self,
        database: PostgresDB,
        server_id: int,
        user_id: int = 0
    ) -> None:
        self.database = database
        self.server_id = server_id
        self.user_id = user_id

        # only attempt to insert the level when both server and user are provided, because not all functions need to be started by a user
        if server_id and user_id:
            await self.database.execute(
                query_name = "insert_unique_row",
                table_name = "level",
                conflict_columns = ["server_id", "user_id"],
                columns = ["server_id", "user_id"],
                values = [str(self.server_id), str(self.user_id)]
            )

    ####################################################################################################

    @staticmethod
    def _calulate_level(total_xp: int) -> int:
        """
        This is the formular to calculate someone's level. Every level has 200xp more xp than the last one following this pattern:

        level = xp | total_xp

        0 = 0    | 0

        1 = 200  | 200

        2 = 400  | 600

        3 = 600  | 1200

        4 = 800  | 2000

        5 = 1000 | 3000

        The formular to get how much xp a level requires is: f(level) = level * 200

        The formular to get how much total xp it requiers to finish a level is: f(level) = 100 * level (level + 1)

        Finally the formular to get from your total xp to your current level: level = math.floor((-1 + √(1 + total_xp/25))/2)
        """

        return math.floor((-1 + math.sqrt(1 + total_xp/25))/2)
    
    ####################################################################################################

    @staticmethod
    def _calulate_xp_until_next_level(total_xp: int, level: int) -> int:
        """The formular to get how much total xp it requiers to finish a level is: f(level) = 100 * level (level + 1)"""

        return (100 * level (level + 1)) - total_xp

    ####################################################################################################

    async def increase_xp(self) -> bool:
        """increase the user's xp and sets a cooldown for earning new xp"""

        if int(time.time()) <= await self.database.fetch_val(
            query_name = "select_where",
            table_name = "level",
            select_columns = ["xp_cooldown"],
            columns = ["server_id", "user_id"],
            values = [str(self.server_id), str(self.user_id)]
        ):
            return False

        await self.database.execute(
            query_name = "increase_total_xp", # this also resets the cooldown
            columns = ["server_id", "user_id"],
            values = [str(self.server_id), str(self.user_id)]
        )

        return True

    ####################################################################################################

    async def get_level_and_xp_until_next(self) -> tuple[int, int]:
        """get the user's level and the xp required until their next level"""

        total_xp = await self.database.fetch_val(
            query_name = "select_where",
            table_name = "level",
            select_columns = ["total_xp"],
            columns = ["server_id", "user_id"],
            values = [str(self.server_id), str(self.user_id)]
        )

        level = self._calulate_level(total_xp)

        return level, self._calulate_xp_until_next_level(total_xp, level)

    ####################################################################################################

    async def get_rank(self) -> int:
        """get the leaderboard position of the user in this server"""

        _, _, rank = await self.database.fetch_row(
            query_name = "select_user_xp_rank",
            limit = 1,
            columns = ["server_id", "user_id"],
            values = [str(self.server_id), str(self.user_id)]
        )

        return rank


    ####################################################################################################

    async def get_all_users_ranked(self, limit: int = 10_000_000) -> list[list[int]]:
        """get a list of lists with user ids, levels and server rank, sorted by most to least total_xp"""

        output: list[list[int]] = []

        async for index, user_rank in enumerate(self.database.fetch_many(
            query_name = "select_user_xp_rank",
            limit = limit,
            columns = ["server_id", "user_id"],
            values = [str(self.server_id), str(self.user_id)]
        )):
            output[index] = [str(user_rank[0]), self._calulate_level(str(user_rank[1])), str(user_rank[2])]

        return sorted(output, key=operator.itemgetter(2))