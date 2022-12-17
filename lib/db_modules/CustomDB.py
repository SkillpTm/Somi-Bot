####################################################################################################

import os
import sqlite3

####################################################################################################



class CustomDB():

    def __init__(self) -> None:
        self.database_path = os.path.join(os.path.dirname(__file__), '../../storage/db/custom_commands.db')

    ####################################################################################################

    def create_table(self,
                     server_id: int) -> None:
        """Creates a table, if there isn't one already"""

        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()

        c.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='server{server_id}'")

        if not c.fetchone():
            c.execute(f"""CREATE TABLE server{server_id} (clean_commandname text,
                                                          commandtext text)""")

            conn.commit()

        conn.close()

    ####################################################################################################

    def create_command(self,
                       server_id: int,
                       clean_commandname: str,
                       commandtext: str) -> bool:
        """This function adds a custom command to the server, if there isn't already a custom command with the same name"""

        self.create_table(server_id)

        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()

        c.execute(f"SELECT clean_commandname FROM server{server_id} WHERE clean_commandname = '{clean_commandname}'")
        
        if c.fetchone():
            conn.close()
            return False

        c.execute(f"INSERT INTO server{server_id} VALUES ('{clean_commandname}', '{commandtext}')")

        conn.commit()

        conn.close()
        return True

    ####################################################################################################

    def delete_command(self, 
                       server_id: int,
                       clean_commandname: str) -> str:
        """This function will delete a custom command, if the command was deleted it will return the commandtext, otherwise an empty string"""

        self.create_table(server_id)

        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()

        c.execute(f"SELECT clean_commandname FROM server{server_id} WHERE clean_commandname = '{clean_commandname}'")

        if not c.fetchone():
            conn.close()
            return ""

        c.execute(f"SELECT commandtext FROM server{server_id} WHERE clean_commandname = '{clean_commandname}'")

        commandtext = c.fetchone()[0]

        c.execute(f"DELETE from server{server_id} WHERE clean_commandname = '{clean_commandname}'")

        conn.commit()

        conn.close()
        return commandtext

    ####################################################################################################

    def list(self,
             server_id: int) -> list | list[str]:
        """This command returns a list of all custom commands a server has. If the server has no custom commands it will retrun an empty list"""

        self.create_table(server_id)

        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()

        c.execute(f"SELECT clean_commandname FROM server{server_id} ORDER BY clean_commandname ASC")

        tuple_all_commandnames = c.fetchall()
        all_commandnames = [commandname[0] for commandname in tuple_all_commandnames]

        conn.close()
        return all_commandnames

    ####################################################################################################

    def get_command_text(self,
                         server_id: int,
                         clean_commandname: str) -> str:
        """This function will get the command text of a custom command, if the input custom command doesn't exist it will return an empty string"""

        self.create_table(server_id)

        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()

        c.execute(f"SELECT clean_commandname FROM server{server_id} WHERE clean_commandname = '{clean_commandname}'")

        if not c.fetchone():
            conn.close()
            return ""

        c.execute(f"SELECT commandtext FROM server{server_id} WHERE clean_commandname = '{clean_commandname}'")

        commandtext = c.fetchone()[0]

        conn.close()
        return commandtext