###package#import###############################################################################

import nextcord

client = nextcord.ext.commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from utilities.maincommands import checks
from utilities.partial_commands import get_user_avatar, embed_builder, deactivate_view_children
from utilities.variables import MODERATOR_ID, AUDIT_LOG_ID



class QuestionShutdown(nextcord.ui.View):
    def __init__(self, interaction):
        self.interaction: nextcord.Interaction = interaction
        super().__init__(timeout = 30)
        self.value = None

    @nextcord.ui.button(label = "Yes", style=nextcord.ButtonStyle.green)
    async def yes_shutown(self,
                          button: nextcord.ui.Button,
                          interaction: nextcord.Interaction):
        self.value = True
        await deactivate_view_children(self)
        self.stop()

    @nextcord.ui.button(label = "No", style=nextcord.ButtonStyle.red)
    async def no_shutdown(self,
                          button: nextcord.ui.Button,
                          interaction: nextcord.Interaction):
        self.value = False
        await deactivate_view_children(self)
        self.stop()

class Shutdown(nextcord.ext.commands.Cog):

    def __init__(self, client):
        self.client = client

    ###shutdown###########################################################

    @nextcord.slash_command(name = "shutdown", description = "[MOD] shuts the bot down")
    @nextcord.ext.application_checks.has_any_role(MODERATOR_ID)
    async def shutdown(self,
                       interaction: nextcord.Interaction):
        if not checks(interaction.guild, interaction.user):
            return

        view = QuestionShutdown(interaction)
        await interaction.response.send_message("Do you really want to shutdown the bot?", view=view, ephemeral=True)
        await view.wait()

        if view.value == None or not view.value:
            await interaction.followup.send("The bot has not been shutdown", ephemeral=True)
            return

        elif view.value:
            print(f"{interaction.user}: /shutdown")

            await interaction.followup.send("The bot is being shutdown", ephemeral=True)

            AUDIT_LOG = self.client.get_channel(AUDIT_LOG_ID)

            member_avatar_url = get_user_avatar(interaction.user)

            embed = embed_builder(color = nextcord.Color.orange(),
                                  author = "Mod Activity",
                                  author_icon = member_avatar_url,
                                  footer = "DEFAULT_KST_FOOTER",

                                  field_one_name = "/shutdown:",
                                  field_one_value = f"{interaction.user.mention} shutdown the bot",
                                  field_one_inline = False)

            await AUDIT_LOG.send(embed=embed)

            uses_update("mod_command_uses", "shutdown")

            await self.client.close()

    @shutdown.error
    async def shutdown_error(self, interaction: nextcord.Interaction, error):
        await interaction.response.send_message(f"Only <@&{MODERATOR_ID}> can use this command.", ephemeral=True)



def setup(client):
    client.add_cog(Shutdown(client))