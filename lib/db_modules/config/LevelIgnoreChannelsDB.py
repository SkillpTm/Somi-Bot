####################################################################################################

import nextcord
import os
import sqlite3

####################################################################################################



class LevelIgnoreChannelsDB():

    def __init__(self) -> None:
        self.database_path = os.path.join(os.path.dirname(__file__), '../../../storage/db/config/level_ignore_channels.db')

    ####################################################################################################

    def create_table(self,
                     server_id: int) -> None:
        """Creates a table, if there isn't one already"""

        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()

        c.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='server{server_id}'")

        if not c.fetchone():
            c.execute(f"CREATE TABLE server{server_id} (channel_id text)")

            conn.commit()

        conn.close()

    ####################################################################################################

    def check_channel_inserted(self,
                               server_id: int,
                               channel_id: int) -> bool:
        """Returns a bool based on if the channel is already in the table"""

        self.create_table(server_id)

        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()

        c.execute(f"SELECT channel_id FROM server{server_id} WHERE channel_id='{channel_id}'")

        if c.fetchone() != None :
            conn.close()

            return True

        conn.close()

        return False

    ####################################################################################################

    def insert_channel(self,
                       server_id: int,
                       channel_id: int) -> None:
        """Inserts a given channel into the table of the server"""

        self.create_table(server_id)

        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()

        c.execute(f"INSERT INTO server{server_id} VALUES ('{channel_id}')")

        conn.commit()

        conn.close()

    ####################################################################################################

    def delete_channel(self,
                       server_id: int,
                       channel_id: int) -> None:
        """Deletes a given channel from the table of the server"""

        self.create_table(server_id)

        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()

        c.execute(f"DELETE from server{server_id} WHERE channel_id = '{channel_id}'")

        conn.commit()

        conn.close()

    ####################################################################################################

    def channels_list(self,
                      server: nextcord.Guild) -> list[int]:
        """Returns a lists of all ignore channels of a server"""

        self.create_table(server.id)

        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()

        c.execute(f"SELECT * FROM server{server.id}")

        ignore_channel_tuple = c.fetchall()
        ignore_channel_ids = [int(channel[0]) for channel in ignore_channel_tuple]

        for ignore_channel_id in ignore_channel_ids:
            if not server.get_channel(ignore_channel_id):
                self.delete_channel(server.id, ignore_channel_id)
                ignore_channel_ids.remove(ignore_channel_id)

        conn.close()

        return ignore_channel_ids