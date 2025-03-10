from lib.db_modules.PostgresDB import PostgresDB



class TelemetryDB():
    """abstraction layer to interact with the telemetry table"""

    def __init__(self, database: PostgresDB) -> None:
        self.database = database
        pass

    ####################################################################################################

    async def increment(self, event: str) -> None:
        """increases amount of uses on the event and inserts it, if not already present"""

        await self.database.execute(query_name="telemetry_increment_amount", values=[event]) # this also inserts the event, if not already present

    ####################################################################################################

    async def get_total_amount(self) -> int:
        """returns the total amount of all telemetry uses (aka all command uses and events happening)"""

        return int(await self.database.fetch_val(query_name="telemetry_total_amount"))