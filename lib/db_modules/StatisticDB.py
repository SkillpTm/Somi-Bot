from lib.db_modules.PostgresDB import PostgresDB



class StatisticDB():
    """
    Abstraction layer to interact with the statistic table.

    On init inserts the user with the server into the "statistic" table, if not already present.
    """

    async def __init__(
        self,
        database: PostgresDB,
        server_id: int,
        user_id: int
    ) -> None:
        self.database = database
        self.server_id = server_id
        self.user_id = user_id

        await self.database.execute(
            query_name = "insert_unique_row",
            table_name = "statistic",
            conflict_columns = ["server_id", "user_id"],
            columns = ["server_id", "user_id"],
            values = [str(self.server_id), str(self.user_id)]
        )

    ####################################################################################################

    async def get(self) -> list[int]:
        """gets all the counts from the db"""

        return await self.database.fetch_row(
            query_name = "insert_row",
            table_name = "statistic",
            select_columns = [
                "attachment_count",
                "char_count",
                "client_command_count",
                "emote_count",
                "link_count",
                "message_count",
                "reply_count",
                "sticker_count",
                "word_count"
            ],
            columns = ["server_id", "user_id"],
            values = [str(self.server_id), str(self.user_id)]
        )

    ####################################################################################################

    async def increase(
        self,
        *,
        attachment_increase: int = 0,
        char_increase: int = 0,
        client_command_increase: int = 0,
        emote_increase: int = 0,
        link_increase: int = 0,
        message_increase: int = 0,
        reply_increase: int = 0,
        sticker_increase: int = 0,
        word_increase: int = 0
    ) -> None:
        """increases all input values by their amount on the db"""

        current_stats = await self.get()

        await self.database.execute(
            query_name = "update_rows_where",
            table_name = "statistic",
            set_columns = [
                "attachment_count",
                "char_count",
                "client_command_count",
                "emote_count",
                "link_count",
                "message_count",
                "reply_count",
                "sticker_count",
                "word_count"
            ],
            set_values = [
                current_stats[0] + attachment_increase,
                current_stats[1] + char_increase,
                current_stats[2] + client_command_increase,
                current_stats[3] + emote_increase,
                current_stats[4] + link_increase,
                current_stats[5] + message_increase,
                current_stats[6] + reply_increase,
                current_stats[7] + sticker_increase,
                current_stats[8] + word_increase
            ],
            columns = ["server_id", "user_id"],
            values = [str(self.server_id), str(self.user_id)]
        )