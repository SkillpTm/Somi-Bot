####################################################################################################

import nextcord
import os
import sqlite3

####################################################################################################



class AuditLogChannelDB():

    def __init__(self) -> None:
        self.database_path = os.path.join(os.path.dirname(__file__), '../../../storage/db/config/audit_log_channel.db')

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

    def insert_channel(self,
                       server_id: int,
                       channel_id: int) -> None:
        """Inserts a given channel id into the table of the server"""

        self.create_table(server_id)

        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()

        c.execute(f"INSERT INTO server{server_id} VALUES ('{channel_id}')")

        conn.commit()

        conn.close()

    ####################################################################################################

    def drop_table(self,
                   server_id: int) -> None:
        """Deletes the table of the server"""

        self.create_table(server_id)

        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()

        c.execute(f"DROP TABLE server{server_id}")

        conn.commit()

        conn.close()

    ####################################################################################################

    def get(self,
            server: nextcord.Guild) -> int | None:
        """Gets the audit log channel of the given server"""

        self.create_table(server.id)

        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()

        c.execute(f"SELECT channel_id FROM server{server.id} WHERE rowid = '1'")

        channel_id = c.fetchone()

        if channel_id:
            channel_id = int(channel_id[0])

            if not server.get_channel(channel_id):
                self.drop_table(server.id)
                channel_id = None

        conn.close()
        
        return channel_id