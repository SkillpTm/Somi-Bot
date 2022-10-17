###package#import###############################################################################

import nextcord
from nextcord import Interaction
from nextcord.ext import commands

client = commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from utilities.maincommands import checks
from utilities.partial_commands import embed_builder
from utilities.variables import XOXO_ID, DUMB_DUMB_ID, WHAT_YOU_WAITING_FOR_ID, BIRTHDAY_ID, OUTTA_MY_HEAD_ID, BOT_COLOR



class levelroles(commands.Cog):

    def __init__(self, client):
        self.client = client

    ###levelroles###########################################################

    @nextcord.slash_command(name = "levelroles", description = "a list and explanation of level roles")
    async def modcommandlist(self,
                             interaction: Interaction):
        if not checks(interaction):
            return

        print(f"{interaction.user}: /leveroles")

        embed = embed_builder(title = "Level Roles",
                              color = BOT_COLOR,
                              footer = "DEFAULT_KST_FOOTER",

                              field_one_name = "What are level roles?",
                              field_one_value = "If you send a message you receive a few xp points. These xp points will eventually make you level up and at certain levels you get level roles. You can see your level by using `_level`",
                              field_one_inline = False,

                              field_two_name = "Role list:",
                              field_two_value = f"Level 40-∞: <@&{XOXO_ID}>\nLevel 30-39: <@&{DUMB_DUMB_ID}>\nLevel 20-29: <@&{WHAT_YOU_WAITING_FOR_ID}>\nLevel 10-19: <@&{BIRTHDAY_ID}>\nLevel 3-9: <@&{OUTTA_MY_HEAD_ID}>",
                              field_two_inline = False,
                              
                              field_three_name = "Perks:",
                              field_three_value = f"These level roles only give you a different color and put you higher on the member's list. The only exception is: From your first level role on (<@&{OUTTA_MY_HEAD_ID}>) you will be allowed to send pictures/video, upload files and your links will have embeds.",
                              field_three_inline = False)

        await interaction.send(embed=embed)

        uses_update("command_uses", "levelroles")

def setup(client):
    client.add_cog(levelroles(client))