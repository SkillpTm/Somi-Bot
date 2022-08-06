###package#import###############################################################################

import nextcord
from nextcord import Color, Embed, Interaction, SlashOption
from nextcord.ext import commands

client = commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################





class (commands.Cog):

    def __init__(self, client):
        self.client = client

<<<<<<< HEAD
    ### ###########################################################

=======
>>>>>>> parent of 322972a (Delete template.py)


def setup(client):
    client.add_cog((client))