####################################################################################################

import sqlite3
import time

####################################################################################################

from lib.db_modules.CommonDB import CommonDB



class ReminderDB(CommonDB):

    def __init__(self,
                 user_id: int) -> None:
        super().__init__(database_path = "../../../storage/db/user_data/reminders.db",
                         table_name = f"user{user_id}",
                         table_structure = """(reminder_time integer,
                                               bot_reply_link text,
                                               delete_id integer,
                                               clean_reminder text)""")

    ####################################################################################################

    def create(self,
               reminder_time: int,
               bot_reply_link: str,
               delete_id: str,
               clean_reminder: str) -> None:
        """This function adds a new """

        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()

        c.execute(f"INSERT INTO {self.table_name} VALUES ('{reminder_time}', '{bot_reply_link}', '{delete_id}', '{clean_reminder}')")

        conn.commit()

        conn.close()

    ####################################################################################################

    def delete(self,
               delete_id: str) -> bool | str:
        """This function deletes a reminder from the user's table. If the delete_id is 'ALL', it will immeaditly return back"""

        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()

        if delete_id == "ALL":
            conn.close()
            return "ALL"

        c.execute(f"SELECT delete_id FROM {self.table_name} WHERE delete_id = '{delete_id}'")

        if not c.fetchone():
            conn.close()
            return False

        c.execute(f"DELETE from {self.table_name} WHERE delete_id = '{delete_id}'")

        conn.commit()

        conn.close()
        return True

    ####################################################################################################

    def delete_all(self) -> None:
        """This function drops a user's reminder table"""

        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()
        
        c.execute(f"DROP TABLE {self.table_name}")

        conn.commit()

        conn.close()

    ####################################################################################################

    def user_list(self) -> list[list[tuple[int, str, int, str]]]:
        """
        This function returns a list of all reminders of a user with the following structure:
        List[List[reminder time, bot reply link, delete id, reminder text]]
        """

        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()

        c.execute(f"SELECT * FROM {self.table_name} ORDER BY reminder_time ASC")
        all_reminders = c.fetchall()

        for index, reminder in enumerate(all_reminders):
            all_reminders[index] = list(reminder)

        conn.close()
        return all_reminders

    ####################################################################################################

    def get_times(self) -> list[list[int, int, int]]:
        """
        This function returns a list of all reminder times, of all users
        List[User[user_id, reminder_time, delete_id]]
        """

        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()

        c.execute("SELECT name FROM sqlite_master WHERE type='table'")
        all_tables = c.fetchall()
        all_users_reminder_times: list[list[int, int, int]] = []

        for user in all_tables:
            c.execute(f"SELECT reminder_time, delete_id FROM {user[0]} ORDER BY reminder_time ASC")
            user_reminder_times = c.fetchall()
            current_time = int(time.time())

            for reminder_time in user_reminder_times:
                if reminder_time[0] > current_time:
                    break
                
                all_users_reminder_times.append([int(user[0][4:]), reminder_time[0], reminder_time[1]])

        conn.close()
        return all_users_reminder_times

    ####################################################################################################

    def get_contents(self, delete_id: int) -> tuple[str, str]:
        """This function returns the reminder and the bot reply link, from a delete id"""

        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()

        c.execute(f"SELECT bot_reply_link, clean_reminder FROM {self.table_name} WHERE delete_id = '{delete_id}'")

        contents = c.fetchone()
        bot_reply_link: str = contents[0]
        reminder_text: str = contents[1]

        conn.close()
        return bot_reply_link, reminder_text