####################################################################################################

import nextcord
import nextcord.ext.commands as nextcord_C
import nextcord.ext.application_checks as nextcord_AC
import os

####################################################################################################

from lib.db_modules import ConfigDB
from lib.modules import Checks, Create, EmbedFunctions
from lib.utilities import SomiBot



class Purge(nextcord_C.Cog):

    def __init__(self, client):
        self.client: SomiBot = client

    ####################################################################################################

    @nextcord.slash_command(name="clear", description="clears the entered amount of messages in a channel", default_member_permissions = nextcord.Permissions(manage_messages=True), name_localizations = {country_tag:"purge" for country_tag in nextcord.Locale})
    @nextcord_AC.check(Checks().interaction_in_guild())
    async def purge(self,
                    interaction: nextcord.Interaction,
                    *,
                    amount: int = nextcord.SlashOption(description="amount of messages to be purged", required=True, min_value=1, max_value=1000)):
        """This command removes the given amount of last messages from a channel."""

        self.client.Loggers.action_log(f"Guild: {interaction.guild.id} ~ Channel: {interaction.channel.id} ~ User: {interaction.user.id} ~ /purge {amount}")

        await interaction.response.defer(ephemeral=True, with_message=True)

        messages = await interaction.channel.purge(limit=amount)

        await interaction.followup.send(embed=EmbedFunctions().success(f"Succesfully purged the last `{amount}` messages from {interaction.channel.mention}."), ephemeral=True)


        if interaction.channel.id in await ConfigDB(interaction.guild.id, "HiddenChannels").get_list(interaction.guild):
            return

        audit_log_id: int = await ConfigDB(interaction.guild.id, "AuditLogChannel").get_list(interaction.guild)

        if not audit_log_id:
            return

        Create().bulk_messages_csv(messages)

        embed = EmbedFunctions().builder(
            color = nextcord.Color.yellow(),
            author = "Mod Activity",
            author_icon = interaction.user.display_avatar,
            footer = "DEFAULT_KST_FOOTER",
            fields = [
                [
                    "/purge:",
                    f"{interaction.user.mention} purged: `{amount} message(s)` in {interaction.channel.mention}",
                    False
                ]
            ]
        )

        audit_log_channel = interaction.guild.get_channel(audit_log_id)
        sent_message = await audit_log_channel.send(embed=embed)
        await sent_message.reply(file=nextcord.File(f"./storage/temp/bulk_messages_{messages[0].guild.id}_{messages[0].channel.id}_{len(messages)}.csv"), mention_author=False)

        os.remove(f"./storage/temp/bulk_messages_{messages[0].guild.id}_{messages[0].channel.id}_{len(messages)}.csv")



def setup(client: SomiBot):
    client.add_cog(Purge(client))