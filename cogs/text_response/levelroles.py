###package#import###############################################################################

import nextcord
from nextcord import Embed, Interaction
from nextcord.ext import commands

client = commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from utilities.maincommands import checks
from utilities.partial_commands import embed_kst_footer
from utilities.variables import XOXO_ID, DUMB_DUMB_ID, WHAT_YOU_WAITING_FOR_ID, BIRTHDAY_ID, OUTTA_MY_HEAD_ID, BOT_COLOR



class levelroles(commands.Cog):

    def __init__(self, client):
        self.client = client

    ###levelroles###########################################################

    @nextcord.slash_command(name = "levelroles", description = "A list and explanation of level roles")
    async def modcommandlist(self,
                             interaction: Interaction):
        if not checks(interaction):
            return

        print(f"{interaction.user}: /leveroles")

        embed = Embed(title="Level Roles",
                      colour=BOT_COLOR)
        embed_kst_footer(embed)

        fields = [("What are level roles?", "If you send a message you receive a few xp points. These xp points will eventually make you level up and at certain levels you get level roles. You can see your level by using `_level`", False),
                  ("Role list:", f"Level 40-∞: <@&{XOXO_ID}>\nLevel 30-39: <@&{DUMB_DUMB_ID}>\nLevel 20-29: <@&{WHAT_YOU_WAITING_FOR_ID}>\nLevel 10-19: <@&{BIRTHDAY_ID}>\nLevel 3-9: <@&{OUTTA_MY_HEAD_ID}>", False),
                  ("Perks:", f"These level roles only give you a different color and put you higher on the members list. The only exception is: From your first level role on (<@&{OUTTA_MY_HEAD_ID}>) you will be allowed to send pictures/video, upload files and your links will have embeds.", False)]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        await interaction.send(embed=embed)

        uses_update("command_uses", "levelroles")

def setup(client):
    client.add_cog(levelroles(client))