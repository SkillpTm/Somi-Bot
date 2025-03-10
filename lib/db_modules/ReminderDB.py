import operator
import time

from lib.db_modules.PostgresDB import PostgresDB



class ReminderDB():
    """Abstraction layer to interact with the reminder table."""

    async def __init__(self, database: PostgresDB, user_id: int = 0) -> None:
        self.database = database
        self.user_id = user_id

    ####################################################################################################

    async def add(
        self,
        reminder_id: str,
        time: int,
        link: str,
        text: str
    ) -> None:
        """adds the reminder to the db"""

        await self.database.execute(
            query_name = "insert_row",
            table_name = "reminder",
            columns = [
                "reminder_id",
                "user_id",
                "time",
                "message_link",
                "message"
            ],
            values = [
                reminder_id,
                str(self.user_id),
                str(time),
                link,
                text
            ]
        )

    ####################################################################################################

    async def delete(self, reminder_id: str) -> bool:
        """deletes the reminder from the db"""

        # check if keyword exists
        if not await self.database.fetch_row(
            query_name = "select_where",
            table_name = "reminder",
            select_columns=["*"],
            columns = ["reminder_id"],
            values = [reminder_id]
        ):
            return False
        
        await self.database.execute(
            query_name = "delete_rows_where",
            table_name = "remidner",
            columns = ["reminder_id"],
            values = [reminder_id]
        )

    ####################################################################################################

    async def delete_all(self) -> None:
        """deletes all the reminder of this user"""

        await self.database.execute(
            query_name = "delete_rows_where",
            table_name = "remidner",
            columns = ["user_id"],
            values = [str(self.user_id)]
        )

    ####################################################################################################

    async def get_reminder(self, reminder_id: str) -> tuple[int, str, str]:
        """get the reminder from reminder_id as: time, message_link, message"""

        output: list[int | str] = await self.database.fetch_row(
            query_name = "select_where",
            table_name = "reminder",
            select_columns=["time", "message_link", "message"],
            columns = ["reminder_id"],
            values = [reminder_id]
        )

        return tuple(*output)

    ####################################################################################################

    async def get_list(self) -> list[list[int | str]]:
        """get a list of lists with all reminder_id, time, message_link, message for the user"""

        output: list[list[int | str]] = []

        async for index, remidner_row in enumerate(self.database.fetch_many(
            query_name = "select_where",
            table_name = "reminder",
            select_columns=[
                "reminder_id",
                "time",
                "message_link",
                "message"
            ],
            columns = ["user_id"],
            values = [str(self.user_id)]
        )):
            output[index] = [int(remidner_row[0]), int(remidner_row[1]), remidner_row[2], remidner_row[3]]

        return sorted(output, key=operator.itemgetter(1))

    ####################################################################################################

    async def get_upcoming(self) -> list[list[int, int]]:
        """get a list of lists with all user's reminders, if the reminder needs to be send out as: reminder_id, user_id"""

        output: list[list[int | str]] = []

        async for remidner_row in self.database.fetch_many(
            query_name = "select_where",
            table_name = "reminder",
            select_columns=[
                "reminder_id",
                "user_id",
                "time"
            ],
            columns = str(1),
            values = [str(1)]
        ):
            if int(remidner_row[2]) <= int(time.time()):
                output.append([int(remidner_row[0]), int(remidner_row[1])])

        return output