####################################################################################################

import os
import sqlite3

####################################################################################################

class CommandUsesDB():

    def __init__(self) -> None:
        self.database_path = os.path.join(os.path.dirname(__file__), '../../storage/db/command_uses.db')

    ####################################################################################################

    def create_table(self,
                     table: str) -> None:
        """Creates a table, if there isn't one already"""

        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()

        c.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")

        if not c.fetchone():
            c.execute(f"""CREATE TABLE {table} (name text,
                                                amount integer)""")

            conn.commit()

        conn.close()

    ####################################################################################################

    def uses_update(self,
                    table: str,
                    column_name: str) -> None:
        """This function adds up how often a command has been used, but adding +1 on every execution"""

        self.create_table(table)

        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()

        c.execute(f"SELECT amount FROM {table} WHERE name = '{column_name}'")

        if not c.fetchone():
            c.execute(f"INSERT INTO {table} VALUES ('{column_name}', 0)")

            conn.commit()

        c.execute(f"SELECT amount FROM {table} WHERE name = '{column_name}'")
        new_amount = c.fetchone()[0] + 1

        c.execute(f"UPDATE {table} SET amount = '{new_amount}' WHERE name = '{column_name}'")

        conn.commit()

        conn.close()

    ####################################################################################################

    def get_total_uses(self,
                       table: str) -> int:
        """This function adds up how often a command has been used, but adding +1 on every execution"""

        self.create_table(table)

        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()

        c.execute(f"SELECT amount FROM {table}")

        all_uses_list: list[tuple[int]] = c.fetchall()

        total_uses = sum([command_uses[0] for command_uses in all_uses_list])

        conn.close()

        return total_uses