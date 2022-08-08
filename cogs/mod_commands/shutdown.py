###package#import###############################################################################

import nextcord
from nextcord import Color, Interaction
from nextcord.ext import application_checks, commands

client = commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from utilities.maincommands import checks
from utilities.partial_commands import get_user_avatar, embed_builder
from utilities.variables import MODERATOR_ID, AUDIT_LOG_ID



class Question_Shutdown(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout = 20)
        self.value = None

    @nextcord.ui.button(label = "Yes", style=nextcord.ButtonStyle.green)
    async def yes_shutown(self,
                          button: nextcord.ui.Button,
                          interaction: Interaction):
        await interaction.send("Bot is being shutdown", ephemeral=True)
        
        self.value = True
        self.stop()

    @nextcord.ui.button(label = "No", style=nextcord.ButtonStyle.red)
    async def no_shutdown(self,
                          button: nextcord.ui.Button,
                          interaction: Interaction):
        await interaction.send("Bot has not been shutdown", ephemeral=True)

        self.value = False
        self.stop()

class shutdown(commands.Cog):

    def __init__(self, client):
        self.client = client

    ###shutdown###########################################################

    @nextcord.slash_command(name = "shutdown", description = "Shuts the bot down")
    @application_checks.has_any_role(MODERATOR_ID)
    async def shutdown(self,
                       interaction: Interaction):
        if not checks(interaction):
            return

        view = Question_Shutdown()
        await interaction.response.send_message("Do you really want to shutdown the bot?", view=view, ephemeral=True, delete_after=20)
        await view.wait()

        if view.value is None:
            await interaction.send("Bot has not been shutdown", ephemeral=True)
            return

        elif view.value:
            print(f"{interaction.user}: /shutdown")

            AUDIT_LOG = self.client.get_channel(AUDIT_LOG_ID)

            member_avatar_url = get_user_avatar(interaction.user)

            embed = embed_builder(color = Color.orange(),
                                  author = "Mod Activity",
                                  author_icon = member_avatar_url,

                                  field_one_name = "/shutdown:",
                                  field_one_value = f"{interaction.user.mention} shutdown the bot",
                                  field_one_inline = False)

            await AUDIT_LOG.send(embed=embed)

            uses_update("mod_command_uses", "shutdown")

            await self.client.close()

    @shutdown.error
    async def shutdown_error(self, interaction: Interaction, error):
        await interaction.response.send_message(f"Only <@&{MODERATOR_ID}> can use this command", ephemeral=True)

def setup(client):
    client.add_cog(shutdown(client))