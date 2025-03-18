from lib.dbModules.PostgresDB import PostgresDB



class CustomCommandDB():
    """Abstraction layer to interact with the custom_command table."""

    def __init__(self, database: PostgresDB, server_id: int) -> None:
        self.database = database
        self.server_id = server_id

    ####################################################################################################
        
    async def add(self, name: str, text: str) -> bool:
        """checks if this server already has a command by this name, if not adds it to the db"""

        # check if a command with that name already exists
        if await self.database.fetch_row(
            query_name = "select_where",
            table_name = "custom_command",
            select_columns = ["*"],
            columns = ["server_id", "command_name"],
            values = [self.server_id, name]
        ):
            return False

        await self.database.execute(
            query_name = "insert_row",
            table_name = "custom_command",
            columns = [
                "server_id",
                "command_name",
                "command_text"
            ],
            values = [
                self.server_id,
                name,
                text
            ]
        )

        return True

    ####################################################################################################
        
    async def delete(self, name: str) -> str:
        """deletes the command from the table and returns its text if deleted"""

        text: str = await self.database.fetch_val(
            query_name = "select_where",
            table_name = "custom_command",
            select_columns = ["command_text"],
            columns = ["server_id", "command_name"],
            values = [self.server_id, name]
        )

        if not text:
            return ""
        
        await self.database.execute(
            query_name = "delete_rows_where",
            table_name = "custom_command",
            columns = ["server_id", "command_name"],
            values = [self.server_id, name]
        )

        return text

    ####################################################################################################
        
    async def delete_all(self) -> None:
        """deletes all commands of this server from the table"""

        await self.database.execute(
            query_name = "delete_rows_where",
            table_name = "custom_command",
            columns = ["server_id"],
            values = [self.server_id]
        )


    ####################################################################################################
        
    async def get_text(self, name: str) -> str:
        """get the output text for a command"""

        return await self.database.fetch_val(
            query_name = "select_where",
            table_name = "custom_command",
            select_columns = ["command_text"],
            columns = ["server_id", "command_name"],
            values = [self.server_id, name]
        )

    ####################################################################################################

    async def get_list(self) -> list[str]:
        """get all command names for the server"""

        return await self.database.fetch_row(
            query_name = "select_where",
            table_name = "custom_command",
            select_columns = ["command_name"],
            columns = ["server_id"],
            values = [self.server_id]
        )