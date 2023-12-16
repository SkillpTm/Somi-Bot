####################################################################################################

import os
import sqlite3

####################################################################################################

from lib.db_modules.CommonDB import CommonDB



class CommandUsesDB():

    def __init__(self,
                 table_name: str) -> None:
        self.database_path = os.path.join(os.path.dirname(__file__), '../../storage/db/command_uses.db')

        self.table_name = table_name
        self.table_structure = """(name text,
                                   amount integer)"""

        CommonDB.create_table(self.table_name, self.database_path, self.table_structure)

    ####################################################################################################

    def uses_update(self,
                    column_name: str) -> None:
        """This function adds up how often a command has been used, but adding +1 on every execution"""

        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()

        c.execute(f"SELECT amount FROM {self.table_name} WHERE name = '{column_name}'")

        if not c.fetchone():
            c.execute(f"INSERT INTO {self.table_name} VALUES ('{column_name}', 0)")

            conn.commit()

        c.execute(f"SELECT amount FROM {self.table_name} WHERE name = '{column_name}'")
        new_amount = c.fetchone()[0] + 1

        c.execute(f"UPDATE {self.table_name} SET amount = '{new_amount}' WHERE name = '{column_name}'")

        conn.commit()

        conn.close()

    ####################################################################################################

    def get_total_uses(self) -> int:
        """This function adds up how often a command has been used, but adding +1 on every execution"""

        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()

        c.execute(f"SELECT amount FROM {self.table_name}")

        all_uses_list: list[tuple[int]] = c.fetchall()

        total_uses = sum([command_uses[0] for command_uses in all_uses_list])

        conn.close()

        return total_uses