###package#import###############################################################################

import nextcord
from nextcord import Embed, Interaction
from nextcord.ext import commands

client = commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from cogs._global_data.global_data import start_time
from database.database_command_uses import uses_update
from utilities.maincommands import checks
from utilities.partial_commands import embed_kst_footer
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

        embed = Embed(title = "Information",
                        description = f"""{self.client.user.mention} is a themed bot after the kpop soloist Jeon Somi written in Python using the [Nextcord API wrapper](https://asyncpraw.readthedocs.io/en/stable/).
                                           Originally it was created to fullfil all needs of [Somicord]({SOMICORD_INVITE}).""",
                        colour=BOT_COLOR)

        embed_kst_footer(embed)
        embed.set_author(name= f"{self.client.user}", icon_url = self.client.user.avatar)
        fields = [("Created by:", f"<@{SKILLP_ID}>", True),
                  ("Current version:", f"{CURRENT_VERSION}", True),
                  ("Uptime:", f"<t:{start_time}:R>", True),
                  ("Invite:", f"This bot was created with a singular server in mind, meaning it isn't made to work in different servers at the same time. There are currently no plans to change this. For more information please message <@{SKILLP_ID}>", False),
                  ("Issues:", "You can report bugs with /bugs and make suggestions with /suggestions!", False)]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

        uses_update("command_uses", "about")

def setup(client):
    client.add_cog(about(client))