from lib.dbModules.PostgresDB import PostgresDB



class ServerDB():
    """Abstraction layer to interact with the server table."""

    def __init__(self, database: PostgresDB, server_id: int) -> None:
        self.database = database
        self.server_id = server_id

    ####################################################################################################

    async def audit_log_set(self, audit_log_channel_id: int) -> None:
        """adds the audit log to the server in the db"""

        await self.database.execute(
            query_name = "update_rows_where",
            table_name = "server",
            columns = ["server_id"],
            values = [self.server_id],
            set_columns = ["audit_log_channel_id"],
            set_values = [audit_log_channel_id]
        )

    ####################################################################################################

    async def audit_log_reset(self) -> bool:
        """deletes the audit log from the server in the db"""

        if not await self.audit_log_get():
            return False

        await self.audit_log_set(None)
        return True
    
    ####################################################################################################

    async def audit_log_get(self) -> int:
        """get the audit log from the db"""

        return await self.database.fetch_val(
            query_name = "select_where",
            table_name = "server",
            select_columns=["audit_log_channel_id"],
            columns = ["server_id"],
            values = [self.server_id]
        )
    
    ####################################################################################################

    async def default_role_set(self, default_role_id: int) -> None:
        """adds the default role to the server in the db"""

        await self.database.execute(
            query_name = "update_rows_where",
            table_name = "server",
            columns = ["server_id"],
            values = [self.server_id],
            set_columns = ["default_role_id"],
            set_values = [default_role_id]
        )

    ####################################################################################################

    async def default_role_reset(self) -> bool:
        """deletes the default role from the server in the db"""

        if not await self.default_role_get():
            return False

        await self.default_role_set(None)
        return True
    
    ####################################################################################################

    async def default_role_get(self) -> int:
        """get the default role from the db"""

        return await self.database.fetch_val(
            query_name = "select_where",
            table_name = "server",
            select_columns=["default_role_id"],
            columns = ["server_id"],
            values = [self.server_id]
        )