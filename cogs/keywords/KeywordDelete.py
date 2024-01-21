####################################################################################################

import nextcord
import nextcord.ext.commands as nextcord_C
import nextcord.ext.application_checks as nextcord_AC

####################################################################################################

from lib.db_modules import KeywordDB
from lib.modules import Checks, EmbedFunctions, Get
from lib.utilities import SomiBot, YesNoButtons



class KeywordDelete(nextcord_C.Cog):

    def __init__(self, client):
        self.client: SomiBot = client

    from lib.utilities.main_commands import keyword

    ####################################################################################################

    @keyword.subcommand(name = "delete", description = "delete a keyword from your keyword list")
    @nextcord_AC.check(Checks().interaction_in_guild())
    async def keyword_delete(self,
                             interaction: nextcord.Interaction,
                             *,
                             keyword: str = nextcord.SlashOption(description="the keyword to be deleted or 'ALL'", required=True, min_length=2, max_length=50)):
        """This command let's you delete a keyword by it's name or all keywords with 'ALL'"""

        self.client.Loggers.action_log(f"Guild: {interaction.guild.id} ~ Channel: {interaction.channel.id} ~ User: {interaction.user.id} ~ /keyword delete {keyword}")

        await interaction.response.defer(ephemeral=True, with_message=True)

        if not KeywordDB(interaction.guild.id, interaction.user.id).get_list():
            await interaction.followup.send(embed=EmbedFunctions().error("You don't have any keywords.\nTo add a keyword use `/keyword add`."), ephemeral=True)
            return


        if keyword == "ALL":
            view = YesNoButtons(interaction=interaction)
            await interaction.followup.send(embed=EmbedFunctions().info_message("Do you really want to delete **ALL** your keywords __**(they can't be recovered)**__?", self.client), view=view, ephemeral=True)
            await view.wait()

            if not view.value:
                await interaction.followup.send(embed=EmbedFunctions().error("Your keywords have **not** been deleted!"), ephemeral=True)
                return

            elif view.value:
                KeywordDB(interaction.guild.id, interaction.user.id).delete_all()

                self.client.Loggers.action_log(f"Guild: {interaction.guild.id} ~ Channel: {interaction.channel.id} ~ User: {interaction.user.id} ~ /reminder delete {keyword} went through")

                await interaction.followup.send(embed=EmbedFunctions().success("**ALL** your keywords have been deleted!"), ephemeral=True)
                return


        keyword = keyword.lower().replace(" ", "")

        deleted = KeywordDB(interaction.guild.id, interaction.user.id).delete(keyword)

        if not deleted:
            await interaction.followup.send(embed=EmbedFunctions().error(f"You don't have a keyword called `{keyword}`.\nTo get a list of your keywords use `/keyword list`."), ephemeral=True)
            return

        await interaction.followup.send(embed=EmbedFunctions().success(f"`{keyword}` has been deleted from your keywords."), ephemeral=True)

    ####################################################################################################

    @keyword_delete.on_autocomplete("keyword")
    async def autocomplete_keyword_delete(self,
                                          interaction: nextcord.Interaction,
                                          keyword: str):
        all_user_keywords = KeywordDB(interaction.guild.id, interaction.user.id).get_list()

        all_user_keywords_dict = {user_keyword: user_keyword for user_keyword in all_user_keywords}

        autocomplete_dict = Get().autocomplete_dict_from_search_string(keyword, all_user_keywords_dict)

        await interaction.response.send_autocomplete(autocomplete_dict)



def setup(client: SomiBot):
    client.add_cog(KeywordDelete(client))