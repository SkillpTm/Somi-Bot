import nextcord

from lib.database import db, Order, Table


class LevelRoles():
    """Helper class holding level role related methodes"""

    @staticmethod
    async def update_users(
        server: nextcord.Guild,
        members_and_xp: list[dict[Table, int]] = [] # [[member_id, level], ...]
    ) -> None:
        """This function checks for the inputed users (or all users of a guild), if they have the correct levelrole.
           If they don't, it findes out, which level role they should have and applys it."""

        # a list of lists all level roles this server has [[role_id, level], ...], sorted by accending levels
        if not (all_level_roles := await db.LevelRole._.get_all(
            [db.LevelRole.ID, db.LevelRole.LEVEL],
            {db.LevelRole.SERVER: server.id},
            db.LevelRole.LEVEL,
            Order.ASCENDING
        )):
            return

        members_and_xp = members_and_xp or await db.Level._.get_all([db.Level.USER, db.Level.XP], {db.Level.SERVER: server.id})
        level_role_list: list[nextcord.Role] = []

        for entry in all_level_roles:
            # if a role doesn't exist anymore, don't add it to the list and delete it from the db
            if not (level_role := server.get_role(db.LevelRole.ID.retrieve(entry))):
                await db.LevelRole._.delete(db.LevelRole.ID.retrieve(entry))
                continue

            level_role_list.append(level_role)

        # if a role doesn't exist anymore, these will missmatch, so redo the level roles on everyone
        if len(all_level_roles) != len(level_role_list):
            LevelRoles.update_users(server)
            return


        for member_entry in members_and_xp:
            member = server.get_member(db.Level.USER.retrieve(member_entry))
            member_level = db.Level.get_level(db.Level.XP.retrieve(member_entry))
            new_role_id = 0

            if not member:
                continue

            # loop over all level roles until we find the role the member is supposed to have
            for role_entry in all_level_roles:
                # when the current role is over the user's level, the previous role is the correct one (saved on new_role_id)
                if member_level < db.LevelRole.LEVEL.retrieve(role_entry):
                    break

                new_role_id: int = db.LevelRole.ID.retrieve(role_entry)

            if not new_role_id:
                await member.remove_roles(level_role_list)
                continue

            # remove all the roles, but the "new" one
            await member.remove_roles([level_role.id != new_role_id for level_role in level_role_list])

            # only add the "new" role if the user doesn't have it
            if not [new_role_id == role.id for role in member.roles]:
                await member.add_roles(server.get_role(new_role_id))


    @staticmethod
    async def get_level_range_with_role(guild: nextcord.Guild) -> str:
        """Makes a string of all the level-roles and their ranges, for which they apply"""

        output_role_list = ""
        level_roles: list[dict[str, int]] = [entry async for entry in db.LevelRole._.get_multiple([db.LevelRole.ID, db.LevelRole.LEVEL], guild.id, order_by=db.LevelRole.LEVEL, order=Order.ASCENDING)]

        for index, entry in enumerate(level_roles):
            # if the current and the next role only have a difference of 1 level display it as such
            if db.LevelRole.LEVEL.retrieve(entry) == db.LevelRole.LEVEL.retrieve(level_roles[index+1])-1:
                output_role_list += f"Level {db.LevelRole.LEVEL.retrieve(entry)}: <@&{db.LevelRole.ID.retrieve(entry)}>\n"
                continue

            # if the this is the last level-role add an infinity symbol
            if index+1 == len(level_roles):
                output_role_list += f"Level {db.LevelRole.LEVEL.retrieve(entry)}-∞: <@&{db.LevelRole.ID.retrieve(entry)}>\n"
                break

            # dispaly the range until the next level role
            output_role_list += f"Level {db.LevelRole.LEVEL.retrieve(entry)}-{db.LevelRole.LEVEL.retrieve(level_roles[index+1])-1}: <@&{db.LevelRole.ID.retrieve(entry)}>\n"

        return output_role_list or "`This server doesn't have any level-roles.`"