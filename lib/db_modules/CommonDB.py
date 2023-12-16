####################################################################################################

import sqlite3

####################################################################################################



class CommonDB():

    def __init__(self) -> None:
        pass

    ####################################################################################################

    @staticmethod
    def create_table(table_name: str,
                     database_path: str,
                     table_structure: str) -> None:
        """Creates a table, if there isn't one already"""

        conn = sqlite3.connect(database_path)
        c = conn.cursor()

        c.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")

        if not c.fetchone():
            c.execute(f"""CREATE TABLE {table_name} {table_structure}""")

            conn.commit()

        conn.close()