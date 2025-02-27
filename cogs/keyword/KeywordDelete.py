import nextcord
import nextcord.ext.commands as nextcord_C
import nextcord.ext.application_checks as nextcord_AC

from lib.db_modules import KeywordDB
from lib.modules import Checks, EmbedFunctions, Get
from lib.utilities import SomiBot, YesNoButtons



class KeywordDelete(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    from lib.utilities.main_commands import keyword

    ####################################################################################################

    @keyword.subcommand(name = "delete", description = "delete a keyword from your keyword list")
    @nextcord_AC.check(Checks().interaction_not_by_bot() and Checks().interaction_in_guild)
    async def keyword_delete(
        self,
        interaction: nextcord.Interaction,
        *,
        keyword: str = nextcord.SlashOption(
            description="the keyword to be deleted or 'DELETE_ALL' to delete every keyword",
            required=True,
            min_length=2,
            max_length=50
        )
    ) -> None:
        """This command let's you delete a keyword by it's name or all keywords with 'ALL'"""

        self.client.Loggers.action_log(Get().log_message(
            interaction,
            "/keyword delete",
            {"keyword": keyword}
        ))

        await interaction.response.defer(ephemeral=True, with_message=True)

        if not KeywordDB(interaction.guild.id, interaction.user.id).get_list():
            await interaction.followup.send(embed=EmbedFunctions().error("You don't have any keywords.\nTo add a keyword use `/keyword add`."), ephemeral=True)
            return

        if keyword == "DELETE_ALL":
            self.delete_all()
            return

        keyword = keyword.lower()

        deleted = KeywordDB(interaction.guild.id, interaction.user.id).delete(keyword)

        if not deleted:
            await interaction.followup.send(embed=EmbedFunctions().error(f"You don't have a keyword called `{keyword}`.\nTo get a list of your keywords use `/keyword list`."), ephemeral=True)
            return

        await interaction.followup.send(embed=EmbedFunctions().success(f"`{keyword}` has been deleted from your keywords."), ephemeral=True)

    ####################################################################################################

    @keyword_delete.on_autocomplete("keyword")
    async def autocomplete_keyword_delete(
        self,
        interaction: nextcord.Interaction,
        keyword: str
    ) -> None:
        """provides autocomplete suggestions to discord"""

        all_user_keywords_dict = {user_keyword: user_keyword for user_keyword in KeywordDB(interaction.guild.id, interaction.user.id).get_list()}
        autocomplete_dict = Get().autocomplete_dict_from_search_string(keyword, all_user_keywords_dict)

        await interaction.response.send_autocomplete(autocomplete_dict)

    ####################################################################################################

    async def delete_all(self, interaction: nextcord.Interaction) -> None:
        """asks the user if they want to delete all their keywords and does as answered"""

        view = YesNoButtons(interaction=interaction)
        await interaction.followup.send(embed=EmbedFunctions().info_message("Do you really want to delete **ALL** your keywords __**(they can't be recovered)**__?", self.client), view=view, ephemeral=True)
        await view.wait()

        if not view.value:
            await interaction.followup.send(embed=EmbedFunctions().error("Your keywords have **not** been deleted!"), ephemeral=True)
            return

        KeywordDB(interaction.guild.id, interaction.user.id).delete_all()

        self.client.Loggers.action_log(Get().log_message(
            interaction,
            "/keyword delete",
            {"DELETE_ALL": "deleted"}
        ))

        await interaction.followup.send(embed=EmbedFunctions().success("**ALL** your keywords have been deleted!"), ephemeral=True)
        return


def setup(client: SomiBot) -> None:
    client.add_cog(KeywordDelete(client))