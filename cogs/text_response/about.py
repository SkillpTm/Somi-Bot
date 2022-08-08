###package#import###############################################################################

import nextcord
from nextcord import Interaction
from nextcord.ext import commands

client = commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from cogs._global_data.global_data import start_time
from database.database_command_uses import uses_update
from utilities.maincommands import checks
from utilities.partial_commands import get_user_avatar, embed_builder
from utilities.variables import SKILLP_ID, SOMICORD_INVITE, CURRENT_VERSION, BOT_COLOR



class about(commands.Cog):

    def __init__(self, client):
        self.client = client

    ###about###########################################################

    @nextcord.slash_command(name = "about", description = "Tells you about Somi bot")
    async def about(self,
                    interaction: Interaction):
        if not checks(interaction):
            return

        print(f"{interaction.user}: /about")

        member_avatar_url = get_user_avatar(self.client.user)

        embed = embed_builder(title = "Information",
                              description = f"""{self.client.user.mention} is a themed bot after the kpop soloist Jeon Somi written in Python using the [Nextcord API wrapper](https://docs.nextcord.dev/en/stable/).
                                                Originally it was created to fullfil all needs of [Somicord]({SOMICORD_INVITE}).""",
                              color = BOT_COLOR,
                              author = f"{self.client.user}",
                              author_icon = member_avatar_url,

                              field_one_name = "Created by:",
                              field_one_value = f"<@{SKILLP_ID}>",
                              field_one_inline = True,

                              field_two_name = "Current version:",
                              field_two_value = f"{CURRENT_VERSION}",
                              field_two_inline = True,
                              
                              field_three_name = "Uptime:",
                              field_three_value = f"<t:{start_time}:R>",
                              field_three_inline = True,
                                                
                              field_four_name = "Invite:",
                              field_four_value = f"This bot was created with a singular server in mind, meaning it isn't made to work in different servers at the same time. There are currently no plans to change this. For more information please message <@{SKILLP_ID}>.",
                              field_four_inline = False,
                                                
                              field_five_name = "Issues:",
                              field_five_value = "You can report bugs with /bugs and make suggestions with /suggestions!",
                              field_five_inline = False,)
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

        uses_update("command_uses", "about")

def setup(client):
    client.add_cog(about(client))