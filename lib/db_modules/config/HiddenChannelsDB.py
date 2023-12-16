####################################################################################################

import nextcord
import os
import sqlite3

####################################################################################################

from lib.db_modules.CommonDB import CommonDB



class HiddenChannelsDB():

    def __init__(self,
                 server_id: int) -> None:
        self.database_path = os.path.join(os.path.dirname(__file__), '../../../storage/db/config/hidden_channels.db')

        self.table_name = f"server{server_id}"
        self.table_structure = """(channel_id text)"""
        
        CommonDB.create_table(self.table_name, self.database_path, self.table_structure)

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
        """Gets all hidden-channels of a server"""

        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()

        c.execute(f"SELECT * FROM {self.table_name}")

        tuple_all_channel_ids = c.fetchall()
        hidden_channel_ids = [int(channel_id[0]) for channel_id in tuple_all_channel_ids]

        for hidden_channel_id in hidden_channel_ids:
            if not server.get_channel(hidden_channel_id):
                self.delete_channel(server.id, hidden_channel_id)
                hidden_channel_ids.remove(hidden_channel_id)

        conn.close()

        return hidden_channel_ids