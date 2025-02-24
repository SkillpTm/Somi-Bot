####################################################################################################

import nextcord
import nextcord.ext.commands as nextcord_C
import nextcord.ext.application_checks as nextcord_AC
import os

####################################################################################################

from lib.db_modules import ConfigDB
from lib.modules import Checks, EmbedFunctions
from lib.utilities import SomiBot



class Reload(nextcord_C.Cog):

    def __init__(self, client):
        self.client: SomiBot = client

    ####################################################################################################

    @nextcord.slash_command(name="reload", description="reload the entire bot", guild_ids = [SomiBot.SOMICORD_ID], default_member_permissions=nextcord.Permissions(manage_guild=True))
    @nextcord_AC.check(Checks().interaction_in_guild())
    async def reload(self,
                     interaction: nextcord.Interaction):
        """This command reloads the bot, it can only be executed from a moderator on Somicord."""

        self.client.Loggers.action_log(f"Guild: {interaction.guild.id} ~ Channel: {interaction.channel.id} ~ User: {interaction.user.id} ~ /reload")

        await interaction.response.defer(ephemeral=True, with_message=True)

        if interaction.user.id != self.client.owner_id:
            await interaction.followup.send(embed=EmbedFunctions().error("You aren't the bot's owner"), ephemeral=True)
            return

        for folder in os.listdir(f"./cogs/"):
            if os.path.isdir(f"./cogs/{folder}/"):
                for extension in os.listdir(f"./cogs/{folder}/"):
                    if extension.endswith(".py"):
                        self.client.reload_extension(f'cogs.{folder}.{extension[:-3]}')

        await self.client.sync_application_commands()
                    
        await interaction.followup.send(embed=EmbedFunctions().success("The bot has been reloaded."), ephemeral=True)


        audit_log_id: int = await ConfigDB(interaction.guild.id, "AuditLogChannel").get_list(interaction.guild)

        if not audit_log_id:
            return

        embed = EmbedFunctions().builder(
            color = self.client.MOD_COLOR,
            author = "Mod Activity",
            author_icon = interaction.user.display_avatar,
            fields = [
                [
                    "/reload:",
                    f"{interaction.user.mention} reloaded the bot!",
                    False
                ]
            ]
        )
        
        audit_log_channel = self.client.get_channel(audit_log_id)
        await audit_log_channel.send(embed=embed)



def setup(client: SomiBot):
    client.add_cog(Reload(client))