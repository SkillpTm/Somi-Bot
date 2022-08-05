###package#import###############################################################################

import nextcord
from nextcord import Color, Embed, Interaction
from nextcord.ext import application_checks, commands

client = commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from utilities.maincommands import checks
from utilities.partial_commands import embed_kst_footer, embed_set_mod_author
from utilities.variables import AUDIT_LOG_ID, MODERATOR_ID, SOMMUNGCHI_ID



class close(commands.Cog):

    def __init__(self, client):
        self.client = client

    ###close###########################################################

    @nextcord.slash_command(name="close", description="Takes regular users the sending message permission away.")
    @application_checks.has_any_role(MODERATOR_ID)
    async def close(self,
                    interaction: Interaction):
        if not checks(interaction):
            return

        print(f"{interaction.user}: /close")

        AUDIT_LOG = self.client.get_channel(AUDIT_LOG_ID)
        SOMMUNGCHI = interaction.guild.get_role(SOMMUNGCHI_ID)
        permissions = nextcord.Permissions()

        permissions.update(send_messages = False, send_messages_in_threads = False, add_reactions = False, view_channel = True, change_nickname = True, use_external_emojis = True, use_external_stickers = True, read_message_history = True, use_slash_commands = True, speak = True, stream = True, use_voice_activation = True, request_to_speak = True)
        await SOMMUNGCHI.edit(permissions=permissions)
        await interaction.response.send_message("Closed the server sucessfully.", ephemeral=True)

        embed = Embed(colour=Color.dark_red())
        embed_kst_footer(embed)
        embed_set_mod_author(interaction, embed)
        embed.add_field(name = "/close:", value = f"{interaction.user.mention} closed the server", inline = True)

        await AUDIT_LOG.send(embed=embed, content = f"<@&{MODERATOR_ID}>")

        uses_update("mod_command_uses", "close")

    @close.error
    async def close_error(self, interaction: Interaction, error):
        await interaction.response.send_message(f"Only <@&{MODERATOR_ID}> can use this command", ephemeral=True)

    ###open###########################################################

    @nextcord.slash_command(name="open", description="Gives regular users the sending message permission.")
    @application_checks.has_any_role(MODERATOR_ID)
    async def open(self,
                   interaction: Interaction):
        if not checks(interaction):
            return

        print(f"{interaction.user}: /open")

        AUDIT_LOG = self.client.get_channel(AUDIT_LOG_ID)
        SOMMUNGCHI = interaction.guild.get_role(SOMMUNGCHI_ID)
        permissions = nextcord.Permissions()

        permissions.update(send_messages = True, send_messages_in_threads = True, add_reactions = True, view_channel = True, change_nickname = True, use_external_emojis = True, use_external_stickers = True, read_message_history = True, use_slash_commands = True, speak = True, stream = True, use_voice_activation = True,    request_to_speak = True)
        await SOMMUNGCHI.edit(permissions=permissions)
        await interaction.response.send_message("Re-opened the server sucessfully.", ephemeral=True)

        embed = Embed(colour=Color.dark_red())
        embed_kst_footer(embed)
        embed_set_mod_author(interaction, embed)
        embed.add_field(name = "/open:", value = f"{interaction.user.mention} re-opened the server", inline = True)

        await AUDIT_LOG.send(embed=embed)

        uses_update("mod_command_uses", "open")

    @open.error
    async def open_error(self, interaction: Interaction, error):
        await interaction.response.send_message(f"Only <@&{MODERATOR_ID}> can use this command", ephemeral=True)

def setup(client):
    client.add_cog(close(client))