####################################################################################################

import nextcord
import sqlite3

####################################################################################################

from lib.db_modules.CommonDB import CommonDB



class LevelIgnoreChannelsDB(CommonDB):

    def __init__(self,
                 server_id: int) -> None:
        super().__init__(database_path = "../../../storage/db/config/level_ignore_channels.db",
                         table_name = f"server{server_id}",
                         table_structure = """(channel_id text)""")

    ####################################################################################################

    def check_channel_inserted(self,
                               channel_id: int) -> bool:
        """Returns a bool based on if the channel is already in the table"""

        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()

        c.execute(f"SELECT channel_id FROM {self.table_name} WHERE channel_id='{channel_id}'")

        if c.fetchone() != None :
            conn.close()

            return True

        conn.close()

        return False

    ####################################################################################################

    def insert_channel(self,
                       channel_id: int) -> None:
        """Inserts a given channel into the table of the server"""

        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()

        c.execute(f"INSERT INTO {self.table_name} VALUES ('{channel_id}')")

        conn.commit()

        conn.close()

    ####################################################################################################

    def delete_channel(self,
                       channel_id: int) -> None:
        """Deletes a given channel from the table of the server"""

        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()

        c.execute(f"DELETE from {self.table_name} WHERE channel_id = '{channel_id}'")

        conn.commit()

        conn.close()

    ####################################################################################################

    def channels_list(self,
                      server: nextcord.Guild) -> list[int]:
        """Returns a lists of all ignore channels of a server"""

        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()

        c.execute(f"SELECT * FROM {self.table_name}")

        ignore_channel_tuple = c.fetchall()
        ignore_channel_ids = [int(channel[0]) for channel in ignore_channel_tuple]

        for ignore_channel_id in ignore_channel_ids:
            if not server.get_channel(ignore_channel_id):
                self.delete_channel(server.id, ignore_channel_id)
                ignore_channel_ids.remove(ignore_channel_id)

        conn.close()

        return ignore_channel_ids