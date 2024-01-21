####################################################################################################

import nextcord
import nextcord.ext.commands as nextcord_C
import nextcord.ext.application_checks as nextcord_AC

####################################################################################################

from lib.db_modules import ConfigDB
from lib.modules import Checks, EmbedFunctions
from lib.utilities import SomiBot



class Restart(nextcord_C.Cog):

    def __init__(self, client):
        self.client: SomiBot = client

    ####################################################################################################

    @nextcord.slash_command(name="restart", description="restarts the entire bot", guild_ids = [SomiBot.SOMICORD_ID], default_member_permissions=nextcord.Permissions(manage_guild=True))
    @nextcord_AC.check(Checks().interaction_in_guild())
    async def restart(self,
                      interaction: nextcord.Interaction):
        """This command restarts the bot, it can only be executed from a moderator on Somicord"""

        self.client.Loggers.action_log(f"Guild: {interaction.guild.id} ~ Channel: {interaction.channel.id} ~ User: {interaction.user.id} ~ /restart")
        
        await interaction.response.send_message(embed=EmbedFunctions().success("Restarting bot..."), ephemeral=True)

        audit_log_id: int = await ConfigDB(interaction.guild.id, "AuditLogChannel").get_list(interaction.guild)

        if audit_log_id:
            embed = EmbedFunctions().builder(
                color = self.client.MOD_COLOR,
                author = "Mod Activity",
                author_icon = interaction.user.display_avatar,
                fields = [
                    [
                        "/restart:",
                        f"{interaction.user.mention} restarted the bot.",
                        True
                    ]
                ]
            )

            audit_log_channel = self.client.get_channel(audit_log_id)
            await audit_log_channel.send(embed=embed)
        
        self.client.restart()



def setup(client: SomiBot):
    client.add_cog(Restart(client))