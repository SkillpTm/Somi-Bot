####################################################################################################

import sqlite3

####################################################################################################


from lib.db_modules.CommonDB import CommonDB


class CustomDB(CommonDB):

    def __init__(self,
                 server_id: int) -> None:
        super().__init__(database_path = "../../storage/db/custom_commands.db",
                         table_name = f"server{server_id}",
                         table_structure = """(clean_commandname text,
                                               commandtext text)""")

    ####################################################################################################

    def create_command(self,
                       clean_commandname: str,
                       commandtext: str) -> bool:
        """This function adds a custom command to the server, if there isn't already a custom command with the same name"""

        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()

        c.execute(f"SELECT clean_commandname FROM server{self.table_name} WHERE clean_commandname = '{clean_commandname}'")
        
        if c.fetchone():
            conn.close()
            return False

        c.execute(f"INSERT INTO server{self.table_name} VALUES ('{clean_commandname}', '{commandtext}')")

        conn.commit()

        conn.close()
        return True

    ####################################################################################################

    def delete_command(self,
                       clean_commandname: str) -> str:
        """This function will delete a custom command, if the command was deleted it will return the commandtext, otherwise an empty string"""

        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()

        c.execute(f"SELECT clean_commandname FROM server{self.table_name} WHERE clean_commandname = '{clean_commandname}'")

        if not c.fetchone():
            conn.close()
            return ""

        c.execute(f"SELECT commandtext FROM server{self.table_name} WHERE clean_commandname = '{clean_commandname}'")

        commandtext = c.fetchone()[0]

        c.execute(f"DELETE from server{self.table_name} WHERE clean_commandname = '{clean_commandname}'")

        conn.commit()

        conn.close()
        return commandtext

    ####################################################################################################

    def list(self) -> list | list[str]:
        """This command returns a list of all custom commands a server has. If the server has no custom commands it will retrun an empty list"""

        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()

        c.execute(f"SELECT clean_commandname FROM server{self.table_name} ORDER BY clean_commandname ASC")

        tuple_all_commandnames = c.fetchall()
        all_commandnames = [commandname[0] for commandname in tuple_all_commandnames]

        conn.close()
        return all_commandnames

    ####################################################################################################

    def get_command_text(self,
                         clean_commandname: str) -> str:
        """This function will get the command text of a custom command, if the input custom command doesn't exist it will return an empty string"""

        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()

        c.execute(f"SELECT clean_commandname FROM server{self.table_name} WHERE clean_commandname = '{clean_commandname}'")

        if not c.fetchone():
            conn.close()
            return ""

        c.execute(f"SELECT commandtext FROM server{self.table_name} WHERE clean_commandname = '{clean_commandname}'")

        commandtext = c.fetchone()[0]

        conn.close()
        return commandtext