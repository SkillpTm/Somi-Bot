import math
import typing

from lib.database.DataAccess import DataAccessMixin, Table
from lib.database.Database import Database
from lib.database.Query import Query



class Level(DataAccessMixin):
    ID = "id"
    USER = "user"
    SERVER = "server"
    COOLDOWN = "cooldown"
    XP = "xp"

    _ = ""

    @staticmethod
    def get_table() -> str:
        """returns the table name"""

        return "level"


    @staticmethod
    def make_primary_key(key: int | str | None) -> dict[Table, int | str | None]:
        """creates a primary key dict from the primary key value"""

        return {Level.ID: key}


    @staticmethod
    def get_level(total_xp: int) -> int:
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

        The formular to get how much total xp it requiers to finish a level is: f(level) = 100 * level * (level + 1)

        Finally the formular to get from your total xp to your current level: level = math.floor((-1 + √(1 + total_xp/25))/2)
        """

        return math.floor((-1 + math.sqrt(1 + total_xp/25))/2)


    @staticmethod
    def get_xp_until_next_level(total_xp: int, level: int) -> int:
        """The formular to get how much total xp it requiers to finish a level is: f(level) = 100 * level * (level + 1)"""

        return (100 * (level + 1) * (level + 2)) - total_xp


    @staticmethod
    async def get_user_rank(where: dict[Table, int | str | None]) -> int:
        """gets the rank of a user in a server"""

        return typing.cast(int, await Database().fetch_val(
            Level.get_table(),
            Query.USER_RANK,
            select = "rank",
            where = {key.value: value for key, value in {Level.SERVER: where[Level.SERVER], Level.USER: where[Level.USER]}.items()} # The order here matters, because of how custom the query is, it can't be properly templated
        ))