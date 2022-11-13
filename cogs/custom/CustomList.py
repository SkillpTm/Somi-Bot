###package#import###############################################################################

import nextcord
from nextcord import Interaction
from nextcord.ext import commands

client = commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from database.database_custom import list_custom
from utilities.maincommands import checks
from utilities.partial_commands import get_user_avatar, embed_builder
from utilities.variables import BOT_COLOR



class custom_list(commands.Cog):

    def __init__(self, client):
        self.client = client

    from utilities.maincommands import custom

    ###custom#list###########################################################

    @custom.subcommand(name = "list", description = "a list of all custom commands on this server")
    async def custom_list(self,
                          interaction: Interaction):
        if not checks(interaction):
            return

        print(f"{interaction.user}: /custom list")

        amount, all_commandnames = list_custom(interaction.guild.id)

        if amount == 0:
            await interaction.response.send_message("There are no custom commands on this server.", ephemeral=True)

            uses_update("command_uses", "custom list")

            return

        member_avatar_url = get_user_avatar(interaction.user)
        output = ""
        i = 0

        while i < amount:
            output += f"/cc `{all_commandnames[i]}`\n"
            i += 1

        embed = embed_builder(color = BOT_COLOR,
                              author = f"Custom command list for {interaction.guild}",
                              author_icon = member_avatar_url,
                              footer = "DEFAULT_KST_FOOTER",

                              field_one_name = "Custom commands:",
                              field_one_value = output[:1000],
                              field_one_inline = True)

        await interaction.response.send_message(embed=embed, ephemeral=True)

        uses_update("command_uses", "custom list")

def setup(client):
    client.add_cog(custom_list(client))