####################################################################################################

import sqlite3

####################################################################################################

from lib.db_modules.CommonDB import CommonDB



class CommandUsesDB(CommonDB):

    def __init__(self,
                 table_name: str) -> None:
        super().__init__(database_path = "../../storage/db/command_uses.db",
                         table_name = table_name,
                         table_structure = """(name text,
                                               amount integer)""")

    ####################################################################################################

    def uses_update(self,
                    command_name: str) -> None:
        """This function adds up how often a command has been used, but adding +1 on every execution"""

        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()

        c.execute(f"SELECT amount FROM {self.table_name} WHERE name = '{command_name}'")

        amount = c.fetchone()

        if not amount:
            self.insert(command_name, 0)

            c.execute(f"SELECT amount FROM {self.table_name} WHERE name = '{command_name}'")
            amount = c.fetchone()

        c.execute(f"UPDATE {self.table_name} SET amount = '{amount[0] + 1}' WHERE name = '{command_name}'")

        conn.commit()
        conn.close()

    ####################################################################################################

    def get_total_uses(self) -> int:
        """This function adds up how often a command has been used, but adding +1 on every execution"""

        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()

        c.execute(f"SELECT name FROM sqlite_master WHERE type='table'")

        all_table_names = c.fetchall()
        total_uses = 0

        for table_name in all_table_names:
            
            c.execute(f"SELECT amount FROM {table_name[0]}")

            all_uses_list: list[tuple[int]] = c.fetchall()
            total_uses += sum([command_uses[0] for command_uses in all_uses_list])

        conn.close()

        return total_uses