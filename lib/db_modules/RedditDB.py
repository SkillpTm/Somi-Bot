####################################################################################################

import os
import sqlite3

####################################################################################################

class RedditDB():

    def __init__(self) -> None:
        self.database_path = os.path.join(os.path.dirname(__file__), '../../storage/db/subreddit_history.db')

    ####################################################################################################

    def create_table(self,
                     sub_reddit: str) -> None:
        """Creates a table, if there isn't one already"""

        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()

        c.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{sub_reddit}'")

        if not c.fetchone():
            c.execute(f"CREATE TABLE {sub_reddit} (id text)")

            conn.commit()

        conn.close()

    ####################################################################################################

    def get_history_ids(self,
                        sub_reddit: str) -> list[str]:
        """This function gets the recent history of the named subreddit"""

        self.create_table(sub_reddit)

        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()

        c.execute(f"SELECT id FROM {sub_reddit} ORDER BY id DESC LIMIT 1000")
        tuple_history_ids = c.fetchall()

        history_ids = [id[0] for id in tuple_history_ids]

        conn.close()

        return history_ids

    ####################################################################################################

    def add_new_id(self,
                   sub_reddit: str,
                   new_id: str) -> None:
        """This function adds a new id into the table of it's subreddit"""

        self.create_table(sub_reddit)

        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()

        c.execute(f"INSERT INTO {sub_reddit} VALUES ('{new_id}')")

        conn.commit()

        conn.close()