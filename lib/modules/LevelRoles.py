import nextcord
import operator

from lib.db_modules.ConfigDB import ConfigDB
from lib.db_modules.LevelsDB import LevelsDB


class LevelRoles():

    def __init__(self) -> None:
        pass

    ####################################################################################################

    async def apply(
        self,
        server: nextcord.Guild,
        members_and_levels: list[list[tuple[int, int]]] = [] # [member_id, level]
    ) -> None:
        """This function checks for the inputed users (or all users of a guild), if they have the correct levelrole.
           If they don't, it findes out, which level role they should have and applys it."""

        # a list of lists all level roles this server has [[role_id, level], ...], sorted by accending levels
        roles_and_levels = sorted(await ConfigDB(server.id, "LevelRoles").get_list(server), key=operator.itemgetter(1))

        if not roles_and_levels:
            return

        if not members_and_levels:
            members_and_levels = LevelsDB(server.id).get_all_user_levels()

        # dict of ID keys and Role objects as values, for easy lookup later: {895475489754890: nextcord.Role, ...}
        ids_and_roles: dict[int, nextcord.Role] = {}

        for role_and_level in roles_and_levels:
            level_role = server.get_role(role_and_level[0])

            # valid that all level roles still exist on the server, if they don't delete them from the db and redo ALL members level roles
            # under normal cuirmenstances this shouldn't have to happen
            if not level_role:
                ConfigDB(server.id, "LevelRoles").delete(role_and_level[0])
                self.apply(server, LevelsDB(server.id).get_all_user_levels())
                return
            
            ids_and_roles[role_and_level[0]] = level_role


        for member_and_level in members_and_levels:
            member, user_level = server.get_member(member_and_level[0]), member_and_level[1]
            new_role_id = 0

            if not member:
                continue

            # loop over all level roles until we find the role the member is supposed to have
            for role_and_level in roles_and_levels:
                role_id, role_level = role_and_level[0], role_and_level[1]

                # when the current role is over the user's level, the previous role is the correct one (saved on new_role_id)
                if user_level < role_level:
                    break

                new_role_id = role_id
            
            if not new_role_id:
                continue

            # this isn't strictly necessary, but ensures there only being one correct level role on the member 
            to_be_removed_roles: list[nextcord.Role] = []

            for level_role_id, level_role in ids_and_roles.keys():
                if level_role_id == new_role_id:
                    await member.add_roles(level_role)
                    continue

                to_be_removed_roles.append(level_role)

            await member.remove_roles(to_be_removed_roles)

    ####################################################################################################

    async def remove_from_members(
        self,
        server: nextcord.Guild,
        role: nextcord.Role
    ) -> None:
        """This function removes a specific levelrole from all members of a guild and then reapplys all current roles with self.apply()"""

        members_without_level_role: list[list[tuple[int, int]]] = []

        for member_and_level in LevelsDB(server.id).get_all_user_levels():
            member = server.get_member(member_and_level[0])

            # we might none, instead of a member
            if not member:
                continue

            if role in member.roles:
                await member.remove_roles(role)
                members_without_level_role.append(member_and_level)

        # reapply all roles for users who need them
        await self.apply(server, members_without_level_role)

    ####################################################################################################

    @staticmethod
    def get_level_range_with_role(level_roles: list[list[tuple[int, int]]]) -> str:
        """Makes a string of all the level-roles and their ranges, for which they apply"""

        output_role_list = ""

        for index, level_role in enumerate(level_roles):
            # if the this is the last level-role add an infinity symbol
            if index+1 == len(level_roles):
                output_role_list += f"Level {level_role[1]}-∞: <@&{level_role[0]}>\n"
                break

            # if the current and the next role only have a difference of 1 level display it as such
            if level_role[1] == level_roles[index+1][1]-1:
                output_role_list += f"Level {level_role[1]}: <@&{level_role[0]}>\n"
                continue

            # dispaly the range until the next level role
            output_role_list += f"Level {level_role[1]}-{level_roles[index+1][1]-1}: <@&{level_role[0]}>\n"

        return output_role_list