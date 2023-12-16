####################################################################################################

import os
import sqlite3

####################################################################################################

from lib.db_modules.CommonDB import CommonDB



class LastFmDB():

    def __init__(self) -> None:
        self.database_path = os.path.join(os.path.dirname(__file__), '../../storage/db/lastfm.db')

        self.table_name = "lastfmUsers"
        self.table_structure = """(discord_user_id text,
                                   lastfm_username text)"""
        
        CommonDB.create_table(self.table_name, self.database_path, self.table_structure)

    ####################################################################################################

    def get_user(self,
                 user_id: int) -> str:
        """This function returna the lf username of a discord user, if they have set one"""

        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()

        c.execute(f"SELECT lastfm_username FROM {self.table_name} WHERE discord_user_id = '{user_id}'")

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

        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()

        c.execute(f"INSERT INTO {self.table_name} VALUES ('{user_id}', '{lastfm_username}')")

        conn.commit()

        conn.close()

    ####################################################################################################

    def reset_user(self,
                   user_id: int) -> None:
        """This function removes a user's info from the db"""

        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()

        c.execute(f"DELETE FROM {self.table_name} WHERE discord_user_id = '{str(user_id)}'")

        conn.commit()

        conn.close()