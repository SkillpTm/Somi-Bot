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

    def update(self,
               command_name: str) -> None:
        """increases the uses count of a command"""

        inserted = self._insert(select_column = "amount",
                                where_column = "name",
                                check_value = command_name,
                                values = [command_name, 0])

        amount = self._get(select_column = "amount",
                           where_column = "name",
                           check_value = command_name)

        self.cur.execute(f"""UPDATE {self.table_name}
                             SET amount = '{amount[0] + 1}'
                             WHERE name = '{command_name}'""")

        self._close(commit = True)

    ####################################################################################################

    def get_total(self) -> int:
        """calulates the total command uses of all commands on all tables"""

        self.cur.execute(f"""SELECT name
                             FROM sqlite_master
                             WHERE type='table'""")

        all_table_names = self.cur.fetchall()
        total_uses = 0

        for table_name in all_table_names:
            self.cur.execute(f"""SELECT amount
                                 FROM {table_name[0]}""")

            all_uses_list: list[tuple[int]] = self.cur.fetchall()
            total_uses += sum([command_uses[0] for command_uses in all_uses_list])

        self._close(commit = False)

        return total_uses