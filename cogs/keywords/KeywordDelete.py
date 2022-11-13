###package#import###############################################################################

import nextcord

client = nextcord.ext.commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from database.database_keywords import delete_keyword, delete_all_user_keywords, list_keyword
from utilities.maincommands import checks
from utilities.partial_commands import string_search_to_list, deactivate_view_children



class QuestionDeleteAllKeywords(nextcord.ui.View):
    def __init__(self, interaction):
        self.interaction: nextcord.Interaction = interaction
        super().__init__(timeout = 30)
        self.value = None

    @nextcord.ui.button(label = "Yes", style=nextcord.ButtonStyle.green)
    async def yes_modmail(self,
                          button: nextcord.ui.Button,
                          interaction: nextcord.Interaction):
        self.value = True
        await deactivate_view_children(self)
        self.stop()

    @nextcord.ui.button(label = "No", style=nextcord.ButtonStyle.red)
    async def no_modmail(self,
                         button: nextcord.ui.Button,
                         interaction: nextcord.Interaction):
        self.value = False
        await deactivate_view_children(self)
        self.stop()

    async def on_timeout(self):
        await deactivate_view_children(self)



class KeywordDelete(nextcord.ext.commands.Cog):

    def __init__(self, client):
        self.client = client

    from utilities.maincommands import keyword

    ###keyword#delete###########################################################

    @keyword.subcommand(name = "delete", description = "delete a keyword from your keyword list")
    async def keyword_delete(self,
                             interaction: nextcord.Interaction,
                             *,
                             keyword: str = nextcord.SlashOption(description="the keyword to be deleted or 'ALL'", required=True, min_length=2, max_length=32)):
        if not checks(interaction.guild, interaction.user):
            return

        print(f"{interaction.user}: /keyword delete {keyword}")

        if not keyword == "ALL":
            clean_keyword = str(keyword.lower().replace(" ", ""))
        else:
            clean_keyword = str(keyword)

        deleted_status = delete_keyword(interaction.user.id, clean_keyword)



        if deleted_status == "ALL":
            view = QuestionDeleteAllKeywords(interaction)
            await interaction.response.send_message("Do you really want to delete **ALL** your __keywords__ (they can't be recovered)?", view=view, ephemeral=True)
            await view.wait()

            if view.value == None or view.value == False:
                await interaction.followup.send("Your __keywords__ have **not** been deleted!", ephemeral=True)
                return

            elif view.value:
                deleted_all = delete_all_user_keywords(interaction.user.id)

                if not deleted_all:
                    await interaction.followup.send("You don't have any keywords.", ephemeral=True)
                    return

                print(f"{interaction.user}: /reminder delete {keyword} went through")

                await interaction.followup.send("**ALL** your __keywords__ have been deleted!", ephemeral=True)

                uses_update("command_uses", "keyword delete")
                return



        if not deleted_status:
            await interaction.response.send_message(f"You don't have a keyword called `{clean_keyword}`.", ephemeral=True)
            return

        await interaction.response.send_message(f"`{clean_keyword}` has been removed from your keyword list.", ephemeral=True)

        uses_update("command_uses", "keyword_delete")

    @keyword_delete.on_autocomplete("keyword")
    async def autocomplete_keyword_delete(self,
                                          interaction: nextcord.Interaction,
                                          keyword: str):
        keywords_list = list_keyword(interaction.user.id)

        autocomplete_list = string_search_to_list(keyword, keywords_list)

        await interaction.response.send_autocomplete(autocomplete_list)



def setup(client):
    client.add_cog(KeywordDelete(client))