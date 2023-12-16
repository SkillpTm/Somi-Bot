####################################################################################################

import os
import sqlite3

####################################################################################################



class CommonDB():

    def __init__(self,
                 database_path: str,
                 table_name: str,
                 table_structure: str) -> None:
        self.database_path = os.path.join(os.path.dirname(__file__), database_path)

        self.table_name = table_name
        self.table_structure = table_structure

        self.create_table()

    ####################################################################################################

    def create_table(self) -> None:
        """Creates a table, if there isn't one already"""

        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()

        c.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{self.table_name}'")

        if not c.fetchone():
            c.execute(f"""CREATE TABLE {self.table_name} {self.table_structure}""")

            conn.commit()

        conn.close()