from lib.dbModules.PostgresDB import PostgresDB



class ServerDB():
    """Abstraction layer to interact with the server table."""

    def __init__(self, database: PostgresDB, server_id: int) -> None:
        self.database = database
        self.server_id = server_id

    ####################################################################################################

    async def _get(self, select_columns: list[str]) -> int:
        """get selected column value from the server"""

        return await self.database.fetch_val(
            query_name = "select_where",
            table_name = "server",
            select_columns = select_columns,
            columns = ["server_id"],
            values = [self.server_id]
        )

    ####################################################################################################

    async def _set(self, set_columns: list[str], set_values: list[int]) -> str:
        """set the column values for the server"""

        await self.database.execute(
            query_name = "update_rows_where",
            table_name = "server",
            columns = ["server_id"],
            values = [self.server_id],
            set_columns = set_columns,
            set_values = set_values
        )

    ####################################################################################################

    async def audit_log_get(self) -> int:
        """get the audit log id from the db"""

        return await self._get(["audit_log_channel_id"])

    ####################################################################################################

    async def audit_log_set(self, audit_log_channel_id: int) -> None:
        """adds the audit log id to the server in the db"""

        await self._set(["audit_log_channel_id"], [audit_log_channel_id])

    ####################################################################################################

    async def audit_log_reset(self) -> bool:
        """deletes the audit log id from the server in the db"""

        if not await self.audit_log_get():
            return False

        await self.audit_log_set(0)
        return True

    ####################################################################################################

    async def default_role_get(self) -> int:
        """get the default role id from the db"""

        return await self._get(["default_role_id"])

    ####################################################################################################

    async def default_role_set(self, default_role_id: int) -> None:
        """adds the default role id to the server in the db"""

        await self._set(["default_role_id"], [default_role_id])

    ####################################################################################################

    async def default_role_reset(self) -> bool:
        """deletes the default role id from the server in the db"""

        if not await self.default_role_get():
            return False

        await self.default_role_set(0)
        return True