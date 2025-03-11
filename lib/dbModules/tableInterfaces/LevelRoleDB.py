import operator

from lib.dbModules.PostgresDB import PostgresDB



class LevelRoleDB():
    """Abstraction layer to interact with the level_role table."""

    def __init__(self, database: PostgresDB, server_id: int) -> None:
        self.database = database
        self.server_id = server_id

    ####################################################################################################
        
    async def add(self, role_id: int, level: int) -> bool:
        """checks if this server already has this channel as a level ignore channel, if not adds it to the db"""

        # check, if the role is already used
        if await self.database.fetch_row(
            query_name = "select_where",
            table_name = "level_role",
            select_columns = ["*"],
            columns = ["role_id"],
            values = [role_id]
        ):
            return False
        
        # check, if the level is already used
        if await self.database.fetch_row(
            query_name = "select_where",
            table_name = "level_role",
            select_columns = ["*"],
            columns = ["server_id", "level"],
            values = [self.server_id, level]
        ):
            return False

        await self.database.execute(
            query_name = "insert_row",
            table_name = "level_role",
            columns = ["role_id", "server_id", "level"],
            values = [role_id, self.server_id, level]
        )

        return True

    ####################################################################################################
        
    async def delete(self, role_id: int) -> bool:
        """deletes the role from the table, if present"""

        # check, if the role is a level role
        if not await self.database.fetch_row(
            query_name = "select_where",
            table_name = "level_role",
            select_columns = ["*"],
            columns = ["role_id"],
            values = [role_id]
        ):
            return False

        await self.database.execute(
            query_name = "delete_rows_where",
            table_name = "level_role",
            columns = ["role_id"],
            values = [role_id]
        )

        return True

    ####################################################################################################
        
    async def get_list(self) -> list[list[int]]:
        """get a list of lists of all level role ids and levels in this server, sorted by level, lowest to highest"""

        output: list[list[int]] = []

        async for level_role_row in self.database.fetch_many(
            query_name = "select_where",
            table_name = "level_role",
            select_columns = ["role_id", "level"],
            columns = ["server_id"],
            values = [self.server_id]
        ):
            output.append([int(level_role_row[0]), int(level_role_row[1])])

        return sorted(output, key=operator.itemgetter(1))