####################################################################################################

import nextcord
import os
import sqlite3

####################################################################################################

from lib.db_modules.CommonDB import CommonDB



class DefaultRoleDB():

    def __init__(self,
                 server_id: int) -> None:
        self.database_path = os.path.join(os.path.dirname(__file__), '../../../storage/db/config/default_role.db')

        self.table_name = f"server{server_id}"
        self.table_structure = """(role_id text)"""
        
        CommonDB.create_table(self.table_name, self.database_path, self.table_structure)

    ####################################################################################################

    def insert_role(self,
                    role_id: int) -> None:
        """Inserts a given role into the table of the server"""

        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()

        c.execute(f"INSERT INTO {self.table_name} VALUES ('{role_id}')")

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
        """Gets the default-role of the given server"""

        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()

        c.execute(f"SELECT role_id FROM {self.table_name} WHERE rowid = '1'")

        role_id = c.fetchone()

        if role_id:
            role_id = int(role_id[0])

            if not server.get_role(role_id):
                self.drop_table(server.id)
                role_id = None

        conn.close()
        
        return role_id