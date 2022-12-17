###package#import###############################################################################

import nextcord
import nextcord.ext.commands as nextcord_C
import nextcord.ext.application_checks as nextcord_AC

###self#imports###############################################################################

from lib.db_modules import KeywordDB
from lib.modules import Checks, EmbedFunctions
from lib.utilities import SomiBot



class KeywordList(nextcord_C.Cog):

    def __init__(self, client):
        self.client: SomiBot = client

    from lib.utilities.main_commands import keyword

    ###keyword#list###########################################################

    @keyword.subcommand(name = "list", description = "a list of all your keywords")
    @nextcord_AC.check(Checks().interaction_in_guild())
    async def keyword_list(self,
                           interaction: nextcord.Interaction):
        """This command outputs a list of all keywords a user has"""

        self.client.Loggers.action_log(f"Guild: {interaction.guild.id} ~ Channel: {interaction.channel.id} ~ User: {interaction.user.id} ~ /keyword list")

        await interaction.response.defer(ephemeral=True, with_message=True)

        user_keywords = KeywordDB().user_list(interaction.guild.id, interaction.user.id)

        if user_keywords == []:
            await interaction.followup.send(embed=EmbedFunctions().error("You don't have any keywords.\nTo add a keyword use `/keyword add`."), ephemeral=True)
            return

        output = ""

        for index, keyword in enumerate(user_keywords):
            output += f"{index + 1}. `{keyword}`\n"

        embed = EmbedFunctions().builder(
            color = self.client.BOT_COLOR,
            author = f"Keyword List for: `{interaction.user.display_name}`",
            author_icon = interaction.user.display_avatar,
            footer = "DEFAULT_KST_FOOTER",
            fields = [
                [
                    "Keywords:",
                    output[:1000],
                    True
                ]
            ]
        )

        await interaction.followup.send(embed=embed, ephemeral=True)



def setup(client: SomiBot):
    client.add_cog(KeywordList(client))