####################################################################################################

import nextcord
import os
import sqlite3

####################################################################################################

from lib.db_modules.CommonDB import CommonDB



class LevelRolesDB():

    def __init__(self,
                 server_id: int) -> None:
        self.database_path = os.path.join(os.path.dirname(__file__), '../../../storage/db/config/level_roles.db')

        self.table_name = f"server{server_id}"
        self.table_structure = """(role_id text,
                                   level integer)"""
        
        CommonDB.create_table(self.table_name, self.database_path, self.table_structure)

    ####################################################################################################

    def check_role_or_level_inserted(self,
                                     role_id: int =  None,
                                     level: int = None) -> bool:
        """Returns a bool based on if role/level is already in db"""

        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()

        if role_id != None:
            c.execute(f"SELECT role_id FROM {self.table_name} WHERE role_id='{role_id}'")

            if c.fetchone() != None :
                conn.close()

                return True

        if level != None:
            c.execute(f"SELECT level FROM {self.table_name} WHERE level='{level}'")

            if c.fetchone() != None :
                conn.close()

                return True

        conn.close()

        return False

    ####################################################################################################

    def insert_role(self,
                    role_id: int,
                    level: int) -> None:
        """Inserts a given role and level into the db"""

        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()

        c.execute(f"""INSERT INTO {self.table_name} VALUES ('{role_id}',
                                                            '{level}')""")

        conn.commit()

        conn.close()

    ####################################################################################################

    def delete_role(self,
                    role_id: int) -> None:
        """Deletes a role/level from the db"""

        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()

        c.execute(f"DELETE from {self.table_name} WHERE role_id = '{role_id}'")

        conn.commit()

        conn.close()

    ####################################################################################################

    async def roles_list(self,
                         server: nextcord.Guild) -> list[list[tuple[int, int]]]:
        """Returns a list of lists with role ids and their levels"""

        from lib.modules.LevelRoles import LevelRoles

        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()

        c.execute(f"SELECT * FROM {self.table_name} ORDER BY level ASC")

        levels_and_roles = c.fetchall()
        level_roles = [[int(level_role[0]), level_role[1]] for level_role in levels_and_roles]

        for level_role in level_roles:
            if not server.get_role(level_role[0]):
                LevelRolesDB().delete_role(server.id, level_role[0])
                await LevelRoles().remove_from_members(server, server.get_role(level_role[0]))
                level_roles.remove(level_role)

        conn.close()

        return level_roles