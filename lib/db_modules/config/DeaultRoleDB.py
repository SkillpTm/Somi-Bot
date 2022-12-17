####################################################################################################

import nextcord
import os
import sqlite3

####################################################################################################



class DefaultRoleDB():

    def __init__(self) -> None:
        self.database_path = os.path.join(os.path.dirname(__file__), '../../../storage/db/config/default_role.db')

    ####################################################################################################

    def create_table(self,
                     server_id: int) -> None:
        """Creates a table, if there isn't one already"""

        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()

        c.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='server{server_id}'")

        if not c.fetchone():
            c.execute(f"CREATE TABLE server{server_id} (role_id text)")

            conn.commit()

        conn.close()

    ####################################################################################################

    def insert_role(self,
                    server_id: int,
                    role_id: int) -> None:
        """Inserts a given role into the table of the server"""

        self.create_table(server_id)

        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()

        c.execute(f"INSERT INTO server{server_id} VALUES ('{role_id}')")

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
        """Gets the default-role of the given server"""

        self.create_table(server.id)

        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()

        c.execute(f"SELECT role_id FROM server{server.id} WHERE rowid = '1'")

        role_id = c.fetchone()

        if role_id:
            role_id = int(role_id[0])

            if not server.get_role(role_id):
                self.drop_table(server.id)
                role_id = None

        conn.close()
        
        return role_id