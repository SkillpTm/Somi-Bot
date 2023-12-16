####################################################################################################

import nextcord
import os
import sqlite3

####################################################################################################

from lib.db_modules.CommonDB import CommonDB



class AuditLogChannelDB():

    def __init__(self,
                 server_id: int) -> None:
        self.database_path = os.path.join(os.path.dirname(__file__), '../../../storage/db/config/audit_log_channel.db')

        self.table_name = f"server{server_id}"
        self.table_structure = """(channel_id text)"""
        
        CommonDB.create_table(self.table_name, self.database_path, self.table_structure)

    ####################################################################################################

    def insert_channel(self,
                       channel_id: int) -> None:
        """Inserts a given channel id into the table of the server"""

        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()

        c.execute(f"INSERT INTO {self.table_name} VALUES ('{channel_id}')")

        conn.commit()

        conn.close()

    ####################################################################################################

    def drop_table(self) -> None:
        """Deletes the table of the server"""

        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()

        c.execute(f"DROP TABLE {self.table_name}")

        conn.commit()

        conn.close()

    ####################################################################################################

    def get(self,
            server: nextcord.Guild) -> int | None:
        """Gets the audit log channel of the given server"""

        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()

        c.execute(f"SELECT channel_id FROM {self.table_name} WHERE rowid = '1'")

        channel_id = c.fetchone()

        if channel_id:
            channel_id = int(channel_id[0])

            if not server.get_channel(channel_id):
                self.drop_table(server.id)
                channel_id = None

        conn.close()
        
        return channel_id