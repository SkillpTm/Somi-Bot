###package#import###############################################################################

import csv
import nextcord
from nextcord import Color, Embed, Interaction, SlashOption
from nextcord.ext import application_checks, commands

client = commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from utilities.maincommands import checks
from utilities.variables import AUDIT_LOG_ID, MODERATOR_ID
from utilities.partial_commands import embed_kst_footer, embed_set_mod_author, make_bulk_messages_csv



class purge(commands.Cog):

    def __init__(self, client):
        self.client = client

    ###purge###########################################################

    @nextcord.slash_command(name="purge", description="clears the entered amount of messages")
    @application_checks.has_any_role(MODERATOR_ID)
    async def purge(self,
                    interaction: Interaction,
                    *,
                    amount: int = SlashOption(description="Amount of messages to be purged", required=True)):
        if not checks(interaction):
            return

        print(f"{interaction.user}: /purge {amount}")

        if type(amount) != int:
            await interaction.response.send_message("Make sure that your purge amount is a number!", ephemeral=True)
            return

        AUDIT_LOG = self.client.get_channel(AUDIT_LOG_ID)

        messages = await interaction.channel.purge(limit=amount)
        await interaction.response.send_message(f"Succesfully purged the last `{amount}` messages from {interaction.channel.mention}", ephemeral=True)

        make_bulk_messages_csv(messages)

        embed = Embed(colour=Color.yellow())
        embed_kst_footer(embed)
        embed_set_mod_author(interaction, embed)

        if amount == 1:
            embed.add_field(name = "/purge:", value = f"{interaction.user.mention} purged: `{amount} message` in {interaction.channel.mention}", inline = False)
        else:
            embed.add_field(name = "/purge:", value = f"{interaction.user.mention} purged: `{amount} messages` in {interaction.channel.mention}", inline = False)

        embed.add_field(name = "Note:", value = "It is possible that there is no CSV after this message or that messages are missing. This is due to the messages not being cached anymore. In this case there is nothing I can do.", inline = False)

        await AUDIT_LOG.send(embed=embed)
        await AUDIT_LOG.send(file=nextcord.File("./storage/bulk_messages.csv"))

        uses_update("mod_command_uses", "purge")

    @purge.error
    async def purge_error(self, interaction: Interaction, error):
        await interaction.response.send_message(f"Only <@&{MODERATOR_ID}> can use this command", ephemeral=True)

def setup(client):
    client.add_cog(purge(client))