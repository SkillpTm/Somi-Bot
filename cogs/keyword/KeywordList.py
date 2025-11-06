import nextcord
import nextcord.ext.commands as nextcord_C

from lib.dbModules import DBHandler
from lib.modules import EmbedFunctions, Get
from lib.utilities import SomiBot



class KeywordList(nextcord_C.Cog):

    from cogs.basic.ParentCommand import ParentCommand

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    @ParentCommand.keyword.subcommand(name="list", description="a list of all your keywords")
    async def keyword_list(self, interaction: nextcord.Interaction) -> None:
        """This command outputs a list of all keywords a user has"""

        self.client.logger.action_log(Get.log_message(interaction, "/keyword list"))

        await interaction.response.defer(ephemeral=True, with_message=True)

        if not (user_keywords := await (await DBHandler(self.client.database, server_id=interaction.guild.id, user_id=interaction.user.id).keyword()).get_list()):
            await interaction.followup.send(embed=EmbedFunctions().get_error_message("You don't have any keywords.\nTo add a keyword use `/keyword add`."), ephemeral=True)
            return

        output = ""

        for index, keyword in enumerate(user_keywords):
            output += f"{index + 1}. `{keyword}`\n"

        embed = EmbedFunctions().builder(
            color = self.client.config.BOT_COLOR,
            author = f"Keyword List for: {interaction.user.display_name}",
            author_icon = interaction.user.display_avatar.url,
            fields = [
                [
                    "Keywords:",
                    output,
                    True
                ]
            ]
        )

        await interaction.followup.send(embed=embed, ephemeral=True)



def setup(client: SomiBot) -> None:
    client.add_cog(KeywordList(client))