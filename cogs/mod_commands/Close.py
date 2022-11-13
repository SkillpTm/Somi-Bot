###package#import###############################################################################

import nextcord

client = nextcord.ext.commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from utilities.maincommands import checks
from utilities.partial_commands import get_user_avatar, embed_builder
from utilities.variables import AUDIT_LOG_ID, MODERATOR_ID, SOMMUNGCHI_ID



class Close(nextcord.ext.commands.Cog):

    def __init__(self, client):
        self.client = client

    ###close###########################################################

    @nextcord.slash_command(name="close", description="[MOD] takes all regular users the sending message permission away")
    @nextcord.ext.application_checks.has_permissions(manage_roles=True)
    async def close(self,
                    interaction: nextcord.Interaction):
        if not checks(interaction.guild, interaction.user):
            return

        print(f"{interaction.user}: /close")

        AUDIT_LOG = self.client.get_channel(AUDIT_LOG_ID)
        SOMMUNGCHI = interaction.guild.get_role(SOMMUNGCHI_ID)
        permissions = nextcord.Permissions()

        permissions.update(send_messages = False, send_messages_in_threads = False, add_reactions = False, view_channel = True, change_nickname = True, use_external_emojis = True, use_external_stickers = True, read_message_history = True, use_slash_commands = True, speak = True, stream = True, use_voice_activation = True, request_to_speak = True)
        await SOMMUNGCHI.edit(permissions=permissions)

        await interaction.response.send_message("Closed the server sucessfully.", ephemeral=True)

        member_avatar_url = get_user_avatar(interaction.user)

        embed = embed_builder(color = nextcord.Color.dark_red(),
                              author = "Mod Activity",
                              author_icon = member_avatar_url,
                              footer = "DEFAULT_KST_FOOTER",

                              field_one_name = "/close:",
                              field_one_value = f"{interaction.user.mention} closed the server!",
                              field_one_inline = True)

        await AUDIT_LOG.send(embed=embed, content = f"<@&{MODERATOR_ID}>")

        uses_update("mod_command_uses", "close")

    @close.error
    async def close_error(self, interaction: nextcord.Interaction, error):
        await interaction.response.send_message(f"Only <@&{MODERATOR_ID}> can use this command.", ephemeral=True)

    ###open###########################################################

    @nextcord.slash_command(name="open", description="[MOD] gives all regular users the sending message permission back")
    @nextcord.ext.application_checks.has_permissions(manage_roles=True)
    async def open(self,
                   interaction: nextcord.Interaction):
        if not checks(interaction.guild, interaction.user):
            return

        print(f"{interaction.user}: /open")

        AUDIT_LOG = self.client.get_channel(AUDIT_LOG_ID)
        SOMMUNGCHI = interaction.guild.get_role(SOMMUNGCHI_ID)
        permissions = nextcord.Permissions()

        permissions.update(send_messages = True, send_messages_in_threads = True, add_reactions = True, view_channel = True, change_nickname = True, use_external_emojis = True, use_external_stickers = True, read_message_history = True, use_slash_commands = True, speak = True, stream = True, use_voice_activation = True,    request_to_speak = True)
        await SOMMUNGCHI.edit(permissions=permissions)

        await interaction.response.send_message("Re-opened the server sucessfully.", ephemeral=True)

        member_avatar_url = get_user_avatar(interaction.user)

        embed = embed_builder(color = nextcord.Color.dark_red(),
                              author = "Mod Activity",
                              author_icon = member_avatar_url,
                              footer = "DEFAULT_KST_FOOTER",

                              field_one_name = "/open:",
                              field_one_value = f"{interaction.user.mention} re-opened the server!",
                              field_one_inline = True)

        await AUDIT_LOG.send(embed=embed)

        uses_update("mod_command_uses", "open")

    @open.error
    async def open_error(self, interaction: nextcord.Interaction, error):
        await interaction.response.send_message(f"Only <@&{MODERATOR_ID}> can use this command.", ephemeral=True)



def setup(client):
    client.add_cog(Close(client))