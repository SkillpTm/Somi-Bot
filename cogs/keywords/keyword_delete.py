###package#import###############################################################################

import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands

client = commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from database.database_keywords import delete_keyword, delete_all_user_keywords
from utilities.maincommands import checks



class question_delete_all_keywords(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout = 30)
        self.value = None

    @nextcord.ui.button(label = "Yes", style=nextcord.ButtonStyle.green)
    async def yes_modmail(self,
                          button: nextcord.ui.Button,
                          interaction: Interaction):
        self.value = True
        self.stop()

    @nextcord.ui.button(label = "No", style=nextcord.ButtonStyle.red)
    async def no_modmail(self,
                         button: nextcord.ui.Button,
                         interaction: Interaction):
        self.value = False
        self.stop()



class keyword_delete(commands.Cog):

    def __init__(self, client):
        self.client = client

    from utilities.maincommands import keyword

    ###keyword#delete###########################################################

    @keyword.subcommand(name = "delete", description = "delete a keyword from your keyword list")
    async def keyword_delete(self,
                             interaction: Interaction,
                             *,
                             keyword: str = SlashOption(description="the keyword to be deleted or 'ALL'", required=True, min_length=2, max_length=32)):
        if not checks(interaction):
            return

        print(f"{interaction.user}: /keyword delete {keyword}")

        if not keyword == "ALL":
            clean_keyword = str(keyword.lower().replace(" ", ""))
        else:
            clean_keyword = str(keyword)

        deleted, deleted_all = delete_keyword(interaction.user.id, clean_keyword)



        if deleted_all == "ALL":
            view = question_delete_all_keywords()
            await interaction.response.send_message("Do you really want to delete **ALL** your __keywords__ (they can't be recovered)?", view=view, delete_after=30, ephemeral=True)
            await view.wait()

            if view.value is None:
                await interaction.user.send("Your __keywords__ have **not** been deleted! The buttons stopped working with this message.")
                return
            elif view.value:
                deleted_all = delete_all_user_keywords(interaction.user.id)

                if not deleted_all:
                    await interaction.user.send("You didn't have any keywords.")
                    return

                print(f"{interaction.user}: /reminder delete {keyword} went through")

                await interaction.user.send("**ALL** your __keywords__ have been deleted!")

                uses_update("command_uses", "keyword delete")
                return
            elif not view.value:
                await interaction.user.send("Your __keywords__ have **not** been deleted!")
                return



        if not deleted:
            await interaction.response.send_message(f"You don't have a keyword called `{clean_keyword}`.", ephemeral=True)
            return

        await interaction.response.send_message(f"`{clean_keyword}` has been removed from your keyword list.", ephemeral=True)

        uses_update("command_uses", "keyword_delete")

def setup(client):
    client.add_cog(keyword_delete(client))