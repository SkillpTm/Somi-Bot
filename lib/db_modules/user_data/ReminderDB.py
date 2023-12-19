####################################################################################################

import time

####################################################################################################

from lib.db_modules.CommonDB import CommonDB



class ReminderDB(CommonDB):

    def __init__(self,
                 user_id: int) -> None:
        super().__init__(database_path = "../../storage/db/user_data/reminders.db",
                         table_name = f"user{user_id}",
                         table_structure = """(time integer,
                                               link text,
                                               id integer,
                                               text text)""")

    ####################################################################################################

    def add(self,
            time: int,
            link: str,
            id: str,
            text: str) -> None:
        """adds the reminder to the table"""

        inserted = self._insert(values = [time, link, id, text])

        self._close(commit = inserted)

    ####################################################################################################

    def delete(self,
               id: str) -> bool:
        """deletes the reminder from the table"""

        deleted = self._delete(select_column = "id",
                               where_column = "id",
                               check_value = id)
        
        self._close(commit = deleted)

        return deleted

    ####################################################################################################

    def delete_all(self) -> None:
        """drops the user's table"""

        self._drop()
        self._close(commit = True)

    ####################################################################################################

    def get_reminder(self,
                     id: int) -> tuple[str, str]:
        """get the link and reminder text of the reminder"""

        reminder = self._get(select_column = "link, text",
                             where_column = "id",
                             check_value = str(id),
                             multiple_columns = True)
        
        link: str = reminder[0]
        text: str = reminder[1]

        self._close(commit = False)

        return link, text

    ####################################################################################################

    def get_list(self) -> list[list[tuple[int, str, int, str]]]:
        """get a list of lists with all times, links, ids and texts of the user"""

        reminders = self._get(select_column = "*",
                              order_column = "time",
                              order_type = "ASC",
                              multiple_columns = True,
                              multiple_columns_and_rows = True)
        
        self._close(commit = False)

        return reminders

    ####################################################################################################

    def get_all(self) -> list[list[int, int, int]]:
        """get a list of lists with all user's reminders as: user id, time and id"""

        self.cur.execute("""SELECT name
                            FROM sqlite_master
                            WHERE type='table'""")
        
        all_table_names = self.cur.fetchall()
        all_users_times: list[list[int, int, int]] = []

        for user in all_table_names:
            user = user[0]

            self.cur.execute(f"""SELECT time, id
                                 FROM {user}
                                 ORDER BY reminder_time ASC""")

            user_times_ids = self.cur.fetchall()
            current_time = int(time.time())

            for time_and_id in user_times_ids:
                reminder_time = time_and_id[0]
                id = time_and_id[1]

                if reminder_time > current_time:
                    break
                
                all_users_times.append([int(user[4:]), reminder_time, id])

        self._close(commit = False)

        return all_users_times