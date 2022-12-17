####################################################################################################

import nextcord
import os
import sqlite3

####################################################################################################



class LevelRolesDB():

    def __init__(self) -> None:
        self.database_path = os.path.join(os.path.dirname(__file__), '../../../storage/db/config/level_roles.db')

    ####################################################################################################

    def create_table(self,
                     server_id: int) -> None:
        """Creates a table, if there isn't one already"""

        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()

        c.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='server{server_id}'")

        if not c.fetchone():
            c.execute(f"""CREATE TABLE server{server_id} (role_id text,
                                                          level integer)""")

            conn.commit()

        conn.close()

    ####################################################################################################

    def check_role_or_level_inserted(self,
                                     server_id: int,
                                     role_id: int =  None,
                                     level: int = None) -> bool:
        """Returns a bool based on if role/level is already in db"""

        self.create_table(server_id)

        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()

        if role_id != None:
            c.execute(f"SELECT role_id FROM server{server_id} WHERE role_id='{role_id}'")

            if c.fetchone() != None :
                conn.close()

                return True

        if level != None:
            c.execute(f"SELECT level FROM server{server_id} WHERE level='{level}'")

            if c.fetchone() != None :
                conn.close()

                return True

        conn.close()

        return False

    ####################################################################################################

    def insert_role(self,
                    server_id: int,
                    role_id: int,
                    level: int) -> None:
        """Inserts a given role and level into the db"""

        self.create_table(server_id)

        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()

        c.execute(f"""INSERT INTO server{server_id} VALUES ('{role_id}',
                                                            '{level}')""")

        conn.commit()

        conn.close()

    ####################################################################################################

    def delete_role(self,
                    server_id: int,
                    role_id: int) -> None:
        """Deletes a role/level from the db"""

        self.create_table(server_id)

        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()

        c.execute(f"DELETE from server{server_id} WHERE role_id = '{role_id}'")

        conn.commit()

        conn.close()

    ####################################################################################################

    async def roles_list(self,
                         server: nextcord.Guild) -> list[list[tuple[int, int]]]:
        """Returns a list of lists with role ids and their levels"""

        from lib.modules.LevelRoles import LevelRoles

        self.create_table(server.id)

        conn = sqlite3.connect(self.database_path)
        c = conn.cursor()

        c.execute(f"SELECT * FROM server{server.id} ORDER BY level ASC")

        levels_and_roles = c.fetchall()
        level_roles = [[int(level_role[0]), level_role[1]] for level_role in levels_and_roles]

        for level_role in level_roles:
            if not server.get_role(level_role[0]):
                LevelRolesDB().delete_role(server.id, level_role[0])
                await LevelRoles().remove_from_members(server, server.get_role(level_role[0]))
                level_roles.remove(level_role)

        conn.close()

        return level_roles