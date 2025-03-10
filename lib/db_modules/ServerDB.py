from lib.db_modules.PostgresDB import PostgresDB



class ServerDB():
    """Abstraction layer to interact with the server table."""

    async def __init__(self, database: PostgresDB, server_id: int) -> None:
        self.database = database
        self.server_id = server_id

    ####################################################################################################

    async def audit_log_set(self, audit_log_channel_id: int) -> None:
        """adds the audit log to the server in the db"""

        await self.database.execute(
            query_name = "update_rows_where",
            table_name = "server",
            columns = ["server_id"],
            values = [str(self.server_id)],
            set_columns = ["audit_log_channel_id"],
            set_values = [str(audit_log_channel_id)]
        )

    ####################################################################################################

    async def audit_log_reset(self) -> None:
        """deletes the audit log from the server in the db"""

        return await self.audit_log_set("")
    
    ####################################################################################################

    async def audit_log_get(self) -> str:
        """get the audit log from the db"""

        return await self.database.fetch_val(
            query_name = "select_where",
            table_name = "server",
            select_columns=["audit_log_channel_id"],
            columns = ["server_id"],
            values = [str(self.server_id)]
        )
    
    ####################################################################################################

    async def default_role_set(self, default_role_id: int) -> None:
        """adds the default role to the server in the db"""

        await self.database.execute(
            query_name = "update_rows_where",
            table_name = "server",
            columns = ["server_id"],
            values = [str(self.server_id)],
            set_columns = ["default_role_id"],
            set_values = [str(default_role_id)]
        )

    ####################################################################################################

    async def default_role_reset(self) -> None:
        """deletes the default role from the server in the db"""

        return await self.default_role_set("")
    
    ####################################################################################################

    async def default_role_get(self) -> str:
        """get the default role from the db"""

        return await self.database.fetch_val(
            query_name = "select_where",
            table_name = "server",
            select_columns=["default_role_id"],
            columns = ["server_id"],
            values = [str(self.server_id)]
        )