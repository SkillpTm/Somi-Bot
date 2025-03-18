import nextcord

from lib.dbModules import DBHandler


class LevelRoles():

    def __init__(self) -> None:
        pass

    ####################################################################################################

    async def update_users(
        self,
        client,
        server: nextcord.Guild,
        members_and_levels: list[list[int]] = [] # [[member_id, level], ...]
    ) -> None:
        """This function checks for the inputed users (or all users of a guild), if they have the correct levelrole.
           If they don't, it findes out, which level role they should have and applys it."""

        # a list of lists all level roles this server has [[role_id, level], ...], sorted by accending levels
        all_level_roles = await (await DBHandler(client.PostgresDB, server_id=server.id).level_role()).get_list()

        if not all_level_roles:
            return

        if not members_and_levels:
            members_and_levels = [[member[0], member[1]] for member in await (await DBHandler(client.PostgresDB, server_id=server.id).level()).get_all_users_ranked()]

        level_role_list: list[nextcord.Role] = []

        for level_role_id in all_level_roles:
            level_role = server.get_role(level_role_id[0])

            # if a role doesn't exist anymore, don't add it to the list and delete it from the db
            if not level_role:
                await (await DBHandler(client.PostgresDB, server_id=server.id).level_role()).delete(level_role_id[0])
                continue

            level_role_list.append(level_role)

        # if a role doesn't exist anymore, these will missmatch, so redo the level roles on everyone
        if len(all_level_roles) != len(level_role_list):
            self.update_users(client, server)
            return


        for member_and_level in members_and_levels:
            member, user_level = server.get_member(member_and_level[0]), member_and_level[1]
            new_role_id = 0

            if not member:
                continue

            # loop over all level roles until we find the role the member is supposed to have
            for level_role in all_level_roles:
                role_id, role_level = level_role[0], level_role[1]

                # when the current role is over the user's level, the previous role is the correct one (saved on new_role_id)
                if user_level < role_level:
                    break

                new_role_id = role_id
            
            if not new_role_id:
                continue

            # remove all the roles, but the "new" one
            await member.remove_roles([level_role.id != new_role_id for level_role in level_role_list])

            # only add the "new" role if the user doesn't have it
            if not [new_role_id == role.id for role in member.roles]:
                await member.add_roles(server.get_role(new_role_id))

    ####################################################################################################

    @staticmethod
    def get_level_range_with_role(level_roles: list[list[tuple[int, int]]]) -> str:
        """Makes a string of all the level-roles and their ranges, for which they apply"""

        output_role_list = ""

        for index, level_role in enumerate(level_roles):
            # if the current and the next role only have a difference of 1 level display it as such
            if level_role[1] == level_roles[index+1][1]-1:
                output_role_list += f"Level {level_role[1]}: <@&{level_role[0]}>\n"
                continue

            # if the this is the last level-role add an infinity symbol
            if index+1 == len(level_roles):
                output_role_list += f"Level {level_role[1]}-∞: <@&{level_role[0]}>\n"
                break

            # dispaly the range until the next level role
            output_role_list += f"Level {level_role[1]}-{level_roles[index+1][1]-1}: <@&{level_role[0]}>\n"

        return output_role_list