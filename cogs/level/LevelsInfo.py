####################################################################################################

import nextcord
import nextcord.ext.commands as nextcord_C
import nextcord.ext.application_checks as nextcord_AC

####################################################################################################

from lib.db_modules import LevelIgnoreChannelsDB, LevelRolesDB
from lib.modules import Checks, EmbedFunctions, LevelRoles
from lib.utilities import SomiBot



class LevelsInfo(nextcord_C.Cog):

    def __init__(self, client):
        self.client: SomiBot = client

    from lib.utilities.main_commands import levels

    ####################################################################################################

    @levels.subcommand(name = "info", description = "displays an explanation for levels, a list of ignored channels and levelroles")
    @nextcord_AC.check(Checks().interaction_in_guild())
    async def levels_info(self,
                          interaction: nextcord.Interaction):
        """Displays information about levels and (if existing) shows a list of the levelroles/ignore channels"""

        self.client.Loggers.action_log(f"Guild: {interaction.guild.id} ~ Channel: {interaction.channel.id} ~ User: {interaction.user.id} ~ /levels info")

        await interaction.response.defer(with_message=True)

        level_roles = await LevelRolesDB().roles_list(interaction.guild)

        for level_role in level_roles:
            if not interaction.guild.get_role(level_role[0]):
                LevelRolesDB().delete_role(interaction.guild.id, level_role[0])
                await LevelRoles().remove_from_members(interaction.guild, interaction.guild.get_role(level_role[0]))
                level_roles.remove(level_role)

        output_role_list = LevelRoles().get_level_range_with_role(level_roles)
        ignore_channel_ids = LevelIgnoreChannelsDB().channels_list(interaction.guild)
        output_ignore_channels = ""
            

        for channel_id in ignore_channel_ids:
            output_ignore_channels += f"<#{channel_id}>\n"

        if output_role_list == "":
            output_role_list = "`This server doesn't have any level-roles.`"

        if output_ignore_channels == "":
            output_ignore_channels = "`In this server you can earn XP in all channels`"

        embed = EmbedFunctions().builder(
            color = self.client.BOT_COLOR,
            title = "Level Information",
            footer = "DEFAULT_KST_FOOTER",
            fields = [
                [
                    "What are levels?",
                    "If you send a message you receive a few xp points. These xp points will eventually make you level up. You can see your level by using `/levels rank`",
                    False
                ],

                [
                    "Level-Roles:",
                    output_role_list,
                    False
                ],

                [
                    "No XP Channels:",
                    output_ignore_channels,
                    False
                ]
            ]
        )

        await interaction.followup.send(embed=embed)



def setup(client: SomiBot):
    client.add_cog(LevelsInfo(client))