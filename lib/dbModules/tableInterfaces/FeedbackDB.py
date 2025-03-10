from lib.dbModules.PostgresDB import PostgresDB



class FeedbackDB():
    """Abstraction layer to interact with the feedback table."""

    def __init__(
        self,
        database: PostgresDB,
        server_id: int,
        user_id: int
    ) -> None:
        self.database = database
        self.server_id = server_id
        self.user_id = user_id
        
    ####################################################################################################
        
    async def submit(
        self,
        time: str,
        text: str
    ) -> None:
        """submits the feedbaack to the db"""

        await self.database.execute(
            query_name = "insert_row",
            table_name = "feedback",
            columns = [
                "server_id",
                "user_id",
                "time_stamp",
                "message"
            ],
            values = [
                self.server_id,
                self.user_id,
                time,
                text,
            ]
        )