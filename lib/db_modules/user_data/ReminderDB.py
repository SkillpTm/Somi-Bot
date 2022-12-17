####################################################################################################

import os
import sqlite3
import time

####################################################################################################

class ReminderDB():

    def __init__(self) -> None:
        self.database_path = os.path.join(os.path.dirname(__file__), '../../../storage/db/user_data/reminders.db')

    ####################################################################################################

    def create_table(self,
                     user_id: int) -> None:
        """Creates a table, if there isn't one already"""

        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()

        c.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='user{user_id}'")

        if not c.fetchone():
            c.execute(f"""CREATE TABLE user{user_id} (reminder_time integer,
                                                      bot_reply_link text,
                                                      delete_id integer,
                                                      clean_reminder text)""")

            conn.commit()

        conn.close()

    ####################################################################################################

    def create(self,
               user_id: int,
               reminder_time: int,
               bot_reply_link: str,
               delete_id: str,
               clean_reminder: str) -> None:
        """This function adds a new """

        self.create_table(user_id)

        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()

        c.execute(f"INSERT INTO user{user_id} VALUES ('{reminder_time}', '{bot_reply_link}', '{delete_id}', '{clean_reminder}')")

        conn.commit()

        conn.close()

    ####################################################################################################

    def delete(self,
               user_id: int,
               delete_id: str) -> bool | str:
        """This function deletes a reminder from the user's table. If the delete_id is 'ALL', it will immeaditly return back"""

        self.create_table(user_id)

        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()

        if delete_id == "ALL":
            conn.close()
            return "ALL"

        c.execute(f"SELECT delete_id FROM user{user_id} WHERE delete_id = '{delete_id}'")

        if not c.fetchone():
            conn.close()
            return False

        c.execute(f"DELETE from user{user_id} WHERE delete_id = '{delete_id}'")

        conn.commit()

        conn.close()
        return True

    ####################################################################################################

    def delete_all(self,
                   user_id: int) -> None:
        """This function drops a user's reminder table"""

        self.create_table(user_id)

        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()
        
        c.execute(f"DROP TABLE user{user_id}")

        conn.commit()

        conn.close()

    ####################################################################################################

    def user_list(self,
                  user_id: int) -> list[list[tuple[int, str, int, str]]]:
        """
        This function returns a list of all reminders of a user with the following structure:
        List[List[reminder time, bot reply link, delete id, reminder text]]
        """

        self.create_table(user_id)

        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()

        c.execute(f"SELECT * FROM user{user_id} ORDER BY reminder_time ASC")
        all_reminders = c.fetchall()

        for index, reminder in enumerate(all_reminders):
            all_reminders[index] = list(reminder)

        conn.close()
        return all_reminders

    ####################################################################################################

    def get_times(self) -> list[list[tuple[int, int, int]]]:
        """
        This function returns a list of all reminder times, of all users
        List[User[user_id, reminder_time, delete_id]]
        """

        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()

        c.execute("SELECT name FROM sqlite_master WHERE type='table'")
        all_tables = c.fetchall()
        all_users_reminder_times: list[list[tuple[int, int, int]]] = []

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

    def get_contents(self, user_id, delete_id) -> tuple[str, str]:
        """This function returns the reminder and the bot reply link, from a delete id"""

        self.create_table(user_id)

        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()

        c.execute(f"SELECT bot_reply_link, clean_reminder FROM user{user_id} WHERE delete_id = '{delete_id}'")

        contents = c.fetchone()
        bot_reply_link: str = contents[0]
        reminder_text: str = contents[1]

        conn.close()
        return bot_reply_link, reminder_text