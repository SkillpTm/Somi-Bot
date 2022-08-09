###package#import###############################################################################

import nextcord
from nextcord import Color, Interaction, SlashOption
from nextcord.ext import application_checks, commands

client = commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from utilities.maincommands import checks
from utilities.variables import AUDIT_LOG_ID, MODERATOR_ID
from utilities.partial_commands import get_user_avatar, make_bulk_messages_csv, embed_builder



class purge(commands.Cog):

    def __init__(self, client):
        self.client = client

    ###purge###########################################################

    @nextcord.slash_command(name="purge", description="[MOD] clears the entered amount of messages in a channel")
    @application_checks.has_any_role(MODERATOR_ID)
    async def purge(self,
                    interaction: Interaction,
                    *,
                    amount: int = SlashOption(description="amount of messages to be purged", required=True, min_value=1, max_value=1000)):
        if not checks(interaction):
            return

        print(f"{interaction.user}: /purge {amount}")

        AUDIT_LOG = self.client.get_channel(AUDIT_LOG_ID)

        messages = await interaction.channel.purge(limit=amount)
        await interaction.response.send_message(f"Succesfully purged the last `{amount}` messages from {interaction.channel.mention}", ephemeral=True)

        make_bulk_messages_csv(messages)

        member_avatar_url = get_user_avatar(interaction.user)

        embed = embed_builder(color = Color.yellow(),
                              author = "Mod Activity",
                              author_icon = member_avatar_url,

                              field_one_name = "/purge:",
                              field_one_value = f"{interaction.user.mention} purged: `{amount} message(s)` in {interaction.channel.mention}",
                              field_one_inline = False,
                              
                              field_two_name = "Note:",
                              field_two_value = "It is possible that there is no CSV after this message or that messages are missing. This is due to the messages not being cached anymore. In this case there is nothing I can do.",
                              field_two_inline = False)

        await AUDIT_LOG.send(embed=embed)
        await AUDIT_LOG.send(file=nextcord.File("./storage/bulk_messages.csv"))

        uses_update("mod_command_uses", "purge")

    @purge.error
    async def purge_error(self, interaction: Interaction, error):
        await interaction.response.send_message(f"Only <@&{MODERATOR_ID}> can use this command.", ephemeral=True)

def setup(client):
    client.add_cog(purge(client))