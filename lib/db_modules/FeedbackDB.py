####################################################################################################

import os
import sqlite3

####################################################################################################

class FeedbackDB():

    def __init__(self) -> None:
        self.database_path = os.path.join(os.path.dirname(__file__), '../../storage/db/feedback.db')

    ####################################################################################################

    def create_table(self) -> None:
        """Creates a table, if there isn't one already"""

        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()

        c.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='feedback'")

        if not c.fetchone():
            c.execute(f"""CREATE TABLE feedback (server_id text,
                                                 user_id text,
                                                 user_name text,
                                                 submission_time text,
                                                 feedback text)""")

            conn.commit()

        conn.close()

    ####################################################################################################

    def submit(self, server_id: int, user_id: int, user_name: str, submission_time: str, feedback: str) -> None:
        """This function submits feedback to the db"""

        self.create_table()

        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()

        c.execute(f"INSERT INTO feedback VALUES ('{server_id}', '{user_id}', '{user_name}', '{submission_time}', '{feedback}')")

        conn.commit()

        conn.close()