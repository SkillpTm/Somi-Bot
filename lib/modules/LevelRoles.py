####################################################################################################

import nextcord

####################################################################################################

from lib.db_modules.config.LevelRolesDB import LevelRolesDB
from lib.db_modules.LevelsDB import LevelsDB



class LevelRoles():

    def __init__(self) -> None:
        pass

    ####################################################################################################

    async def apply(self,
                    server: nextcord.Guild,
                    input_users: list[list[tuple[int, int]]] = [[0, 0]]) -> None:
        """This function checks for the inputed users (or all users of a guild), if they have the correct levelrole.
           If they don't, it findes out, which level role they should have and applys it."""

        levelroles = await LevelRolesDB().roles_list(server)
        if input_users == [[0, 0]]:
            input_users = LevelsDB().get_all_user_levels(server.id)

        if levelroles == []:
            return

        server_level_roles: list[nextcord.Role] = [server.get_role(levelrole[0]) for levelrole in levelroles]
        users_and_level_roles = {}

        for levelrole in levelroles:
            for user in input_users:
                if user[1] >= levelrole[1]:
                    users_and_level_roles.update({user[0]: levelrole[0]})

        for user_id, levelrole_id in users_and_level_roles.items():
            member = server.get_member(user_id)
            role = server.get_role(levelrole_id)

            if not role:
                LevelRolesDB().delete_role(server.id, levelrole_id)
                await self.remove_from_members(server, role)
                return

            if hasattr(member, "roles"):
                if not role in member.roles:
                    for server_level_role in server_level_roles:
                        if server_level_role in member.roles:
                            await member.remove_roles(server_level_role)

                    await member.add_roles(role)

    ####################################################################################################

    async def remove_from_members(self,
                                  server: nextcord.Guild,
                                  role: nextcord.Role) -> None:
        """This function removes a specific levelrole from all members of a guild"""

        all_users = LevelsDB().get_all_user_levels(server.id)

        for user in all_users:
            member = server.get_member(user[0])

            if hasattr(member, "roles"):
                if role in member.roles:
                    await member.remove_roles(role)

        await self.apply(server)

    ####################################################################################################

    @staticmethod
    def get_level_range_with_role(level_roles: list[list[tuple[int, int]]]) -> str:
        """Makes a string of all the level-roles and their ranges, for which they apply"""

        output_role_list = ""

        for index, levelrole in enumerate(level_roles):
            if index+1 != len(level_roles):
                if levelrole[1] == level_roles[index+1][1]-1: # if 2 roles only have a difference of 1 level
                    output_role_list += f"Level {levelrole[1]}: <@&{levelrole[0]}>\n"
                else:
                    output_role_list += f"Level {levelrole[1]}-{level_roles[index+1][1]-1}: <@&{levelrole[0]}>\n"
            else: # last level-role
                output_role_list += f"Level {levelrole[1]}-∞: <@&{levelrole[0]}>\n"

        return output_role_list