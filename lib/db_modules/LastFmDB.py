####################################################################################################

import os
import sqlite3

####################################################################################################



class LastFmDB():

    def __init__(self) -> None:
        self.database_path = os.path.join(os.path.dirname(__file__), '../../storage/db/lastfm.db')

    ####################################################################################################

    def create_table(self) -> None:
        """Creates a table, if there isn't one already"""

        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()

        c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='lastfmUsers'")

        if not c.fetchone():
            c.execute("""CREATE TABLE lastfmUsers (discord_user_id text,
                                                   lastfm_username text)""")

            conn.commit()

        conn.close()

    ####################################################################################################

    def get_user(self,
                 user_id: int) -> str:
        """This function returna the lf username of a discord user, if they have set one"""

        self.create_table()

        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()

        c.execute(f"SELECT lastfm_username FROM lastfmUsers WHERE discord_user_id = '{user_id}'")

        lf_user = c.fetchone()

        if not lf_user:
            conn.close()
            return None

        conn.close()
        return lf_user[0]

    ####################################################################################################

    def set_user(self,
                 user_id: int,
                 lastfm_username: str) -> None:
        """This function connects a discord and lastfm user in the db"""

        self.create_table()

        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()

        c.execute(f"INSERT INTO lastfmUsers VALUES ('{user_id}', '{lastfm_username}')")

        conn.commit()

        conn.close()

    ####################################################################################################

    def reset_user(self,
                   user_id: int) -> None:
        """This function removes a user's info from the db"""

        self.create_table()

        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()

        c.execute(f"DELETE FROM lastfmUsers WHERE discord_user_id = '{str(user_id)}'")

        conn.commit()

        conn.close()