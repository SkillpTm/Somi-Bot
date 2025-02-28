import nextcord
import nextcord.ext.commands as nextcord_C
import nextcord.ext.application_checks as nextcord_AC
import re

from lib.db_modules import KeywordDB
from lib.modules import Checks, EmbedFunctions, Get
from lib.utilities import SomiBot



class KeywordAdd(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    from lib.utilities.main_commands import keyword

    ####################################################################################################
    
    @keyword.subcommand(name = "add", description = "add a keyword to your keyword list")
    @nextcord_AC.check(Checks().interaction_not_by_bot() and Checks().interaction_in_guild)
    async def keyword_add(
        self,
        interaction: nextcord.Interaction,
        *,
        keyword: str = nextcord.SlashOption(
            description = "your new keyword",
            required = True,
            min_length = 2,
            max_length = 50
        )
    ) -> None:
        """This command adds a global keyword to the bot for a user"""

        self.client.Loggers.action_log(Get().log_message(
            interaction,
            "/keyword add",
            {"keyword": keyword}
        ))

        await interaction.response.defer(ephemeral=True, with_message=True)

        keyword = keyword.lower()

        # make sure keywords are only letters and numbers
        if not re.match(r"^[\da-z]+$", keyword):
            await interaction.followup.send(embed=EmbedFunctions().error(f"You can only have letters and numbers in your keywords!"), ephemeral=True)
            return

        added = KeywordDB(interaction.guild.id, interaction.user.id).add(keyword)

        if not added:
            await interaction.followup.send(embed=EmbedFunctions().error(f"You already have `{keyword}` as a keyword.\nTo get a list of your keywords use `/keyword list`."), ephemeral=True)
            return

        await interaction.followup.send(embed=EmbedFunctions().success(f"`{keyword}` has been added to your keywords."), ephemeral=True)



def setup(client: SomiBot) -> None:
    client.add_cog(KeywordAdd(client))