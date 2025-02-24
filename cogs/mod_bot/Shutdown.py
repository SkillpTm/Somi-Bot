####################################################################################################

import nextcord
import nextcord.ext.commands as nextcord_C
import nextcord.ext.application_checks as nextcord_AC

####################################################################################################

from lib.db_modules import ConfigDB
from lib.modules import Checks, EmbedFunctions
from lib.utilities import YesNoButtons, SomiBot



class Shutdown(nextcord_C.Cog):

    def __init__(self, client):
        self.client: SomiBot = client

    ####################################################################################################

    @nextcord.slash_command(name = "shutdown", description = "shuts the bot down", guild_ids = [SomiBot.SOMICORD_ID], default_member_permissions=nextcord.Permissions(manage_guild=True))
    @nextcord_AC.check(Checks().interaction_in_guild())
    async def shutdown(self,
                       interaction: nextcord.Interaction):
        """This command let's you shutdown the bot, it can only be executed from a moderator on Somicord."""

        self.client.Loggers.action_log(f"Guild: {interaction.guild.id} ~ Channel: {interaction.channel.id} ~ User: {interaction.user.id} ~ /shutdown")

        await interaction.response.defer(ephemeral=True, with_message=True)

        if interaction.user.id != self.client.owner_id:
            await interaction.followup.send(embed=EmbedFunctions().error("You aren't the bot's owner"), ephemeral=True)
            return

        view = YesNoButtons(interaction=interaction)
        await interaction.followup.send(embed=EmbedFunctions().info_message("Do you really want to shutdown the bot?", self.client), view=view, ephemeral=True)
        await view.wait()

        if not view.value:
            await interaction.followup.send(embed=EmbedFunctions().error("The bot has not been shutdown"), ephemeral=True)
            return

        self.client.Loggers.action_log(f"Guild: {interaction.guild.id} ~ Channel: {interaction.channel.id} ~ User: {interaction.user.id} ~ /shutdown went through")

        await interaction.followup.send(embed=EmbedFunctions().success("The bot is being shutdown..."), ephemeral=True)


        audit_log_id: int = await ConfigDB(interaction.guild.id, "AuditLogChannel").get_list(interaction.guild)

        if audit_log_id:
            embed = EmbedFunctions().builder(
                color = nextcord.Color.orange(),
                author = "Mod Activity",
                author_icon = interaction.user.display_avatar,
                footer = "DEFAULT_KST_FOOTER",
                fields = [
                    [
                        "/shutdown:",
                        f"{interaction.user.mention} shutdown the bot",
                        False
                    ]
                ]
            )

            audit_log_channel = self.client.get_channel(audit_log_id)
            await audit_log_channel.send(embed=embed)

        await self.client.close()



def setup(client: SomiBot):
    client.add_cog(Shutdown(client))