import nextcord
import nextcord.ext.commands as nextcord_C

from lib.dbModules import DBHandler
from lib.managers import Config
from lib.modules import EmbedFunctions, LevelRoles
from lib.utilities import SomiBot



class LevelsInfo(nextcord_C.Cog):

    from cogs.basic.ParentCommand import ParentCommand

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    @ParentCommand.levels.subcommand(name="info", description="displays an explanation for levels, a list of ignored channels and levelroles")
    async def levels_info(self, interaction: nextcord.Interaction) -> None:
        """Displays information about levels and (if existing) shows a list of the levelroles/ignore channels"""

        await interaction.response.defer(with_message=True)

        if not (output_role_list := LevelRoles.get_level_range_with_role(await (await DBHandler(self.client.database, server_id=interaction.guild.id).level_role()).get_list())):
            output_role_list = "`This server doesn't have any level-roles.`"

        if not (output_ignore_channels := "".join(f"<#{channel_id}>\n" for channel_id in await (await DBHandler(self.client.database, server_id=interaction.guild.id).level_ignore_channel()).get_list())):
            output_ignore_channels = "`In this server you can earn XP in all channels`"

        embed = EmbedFunctions().builder(
            color = Config().BOT_COLOR,
            title = "Level Information",
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



def setup(client: SomiBot) -> None:
    client.add_cog(LevelsInfo(client))