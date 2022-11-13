###package#import###############################################################################

import nextcord

client = nextcord.ext.commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from database.database_custom import list_custom
from utilities.maincommands import checks
from utilities.partial_commands import get_user_avatar, embed_builder
from utilities.variables import BOT_COLOR



class CustomList(nextcord.ext.commands.Cog):

    def __init__(self, client):
        self.client = client

    from utilities.maincommands import custom

    ###custom#list###########################################################

    @custom.subcommand(name = "list", description = "a list of all custom commands on this server")
    async def custom_list(self,
                          interaction: nextcord.Interaction):
        if not checks(interaction.guild, interaction.user):
            return

        print(f"{interaction.user}: /custom list")

        all_commandnames = list_custom(interaction.guild.id)

        if len(all_commandnames) == 0:
            await interaction.response.send_message("There are no custom commands on this server.", ephemeral=True)

            uses_update("command_uses", "custom list")

            return

        member_avatar_url = get_user_avatar(interaction.user)
        output = ""

        for commandname in all_commandnames:
            output += f"/cc `{commandname}`\n"

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
    client.add_cog(CustomList(client))