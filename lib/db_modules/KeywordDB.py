from lib.db_modules.PostgresDB import PostgresDB



class KeywordDB():
    """Abstraction layer to interact with the keyword table."""

    async def __init__(
        self,
        database: PostgresDB,
        server_id: int,
        user_id: int
    ) -> None:
        self.database = database
        self.server_id = server_id
        self.user_id = user_id

    ####################################################################################################

    async def add(self, keyword: str) -> bool:
        """checks if this user on this server already has this keyword, if not adds it to the db"""

        # check if a keyword with that name already exists
        if await self.database.fetch_row(
            query_name = "select_where",
            table_name = "keyword",
            select_columns=["*"],
            columns = [
                "server_id",
                "user_id",
                "keyword"
            ],
            values = [
                str(self.server_id),
                str(self.user_id),
                keyword
            ]
        ):
            return False

        await self.database.execute(
            query_name = "insert_row",
            table_name = "keyword",
            columns = [
                "server_id",
                "user_id",
                "keyword"
            ],
            values = [
                str(self.server_id),
                str(self.user_id),
                keyword
            ]
        )

        return True

    ####################################################################################################

    async def delete(self, keyword: str) -> bool:
        """checks if this user on this server has this keyword, if so deletes it from the db"""

        # check if keyword exists
        if not await self.database.fetch_row(
            query_name = "select_where",
            table_name = "keyword",
            select_columns=["*"],
            columns = [
                "server_id",
                "user_id",
                "keyword"
            ],
            values = [
                str(self.server_id),
                str(self.user_id),
                keyword
            ]
        ):
            return False
        
        await self.database.execute(
            query_name = "delete_rows_where",
            table_name = "keyword",
            columns = [
                "server_id",
                "user_id",
                "keyword"
            ],
            values = [
                str(self.server_id),
                str(self.user_id),
                keyword
            ]
        )

        return True

    ####################################################################################################

    async def delete_all(self) -> None:
        """deletes all the keywords of this user on this server"""

        await self.database.execute(
            query_name = "delete_rows_where",
            table_name = "keyword",
            columns = ["server_id", "user_id"],
            values = [str(self.server_id), str(self.user_id)]
        )

    ####################################################################################################

    async def get_list(self) -> list[str]:
        """gets a list with all keywords of the user"""

        output: list[str] = []

        async for keyword_row in self.database.fetch_many(
            query_name = "select_where",
            table_name = "keyword",
            select_columns=["keyword"],
            columns = ["server_id", "user_id"],
            values = [str(self.server_id), str(self.user_id)]
        ):
            output.append(keyword_row[0])

        return sorted(output)

    ####################################################################################################

    async def get_all(self) -> dict[int, list[str]]:
        """gets all users with their keywords from this server, except for the provided user and their keywords"""

        output: dict[int, list[str]] = {}

        async for keyword_row in self.database.fetch_many(
            query_name = "select_where",
            table_name = "keyword",
            select_columns=["user_id", "keyword"],
            columns = ["server_id"],
            values = [str(self.server_id)]
        ): 
            user_id, keyword = int(keyword_row[0]), keyword_row[1]

            # if the keyword is from the message auther don't add them
            if user_id == self.user_id:
                continue

            if user_id not in output.keys():
                output[user_id] = keyword
                continue

            output[user_id].append(keyword)

        # sort the keywords alphabetically
        for user_id in output.keys():
            output[user_id] = sorted(output[user_id])

        return output