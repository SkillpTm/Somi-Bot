###package#import###############################################################################

import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
import random

client = commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from utilities.maincommands import checks



class choose(commands.Cog):

    def __init__(self, client):
        self.client = client

    ###choose###########################################################
    
    @nextcord.slash_command(name = "choose", description = "Let the bot choose one of the options for you!")
    async def choose(self,
                     interaction: Interaction,
                     *,
                     option1: str = SlashOption(description="First Option", required=True, min_length=1, max_length=200),
                     option2: str = SlashOption(description="Second Option", required=True, min_length=1, max_length=200),
                     option3: str = SlashOption(description="Third Option", required=False, min_length=1, max_length=200),
                     option4: str = SlashOption(description="Fourth Option", required=False, min_length=1, max_length=200),
                     option5: str = SlashOption(description="Fifth Option", required=False, min_length=1, max_length=200),
                     option6: str = SlashOption(description="Sixth Option", required=False, min_length=1, max_length=200),
                     option7: str = SlashOption(description="Seventh Option", required=False, min_length=1, max_length=200),
                     option8: str = SlashOption(description="Eigth Option", required=False, min_length=1, max_length=200),
                     option9: str = SlashOption(description="Ninth Option", required=False, min_length=1, max_length=200),
                     option10: str = SlashOption(description="Tenth Option", required=False, min_length=1, max_length=200)):
        if not checks(interaction):
            return

        RawOptions = []
        Options = []
        i = 0

        RawOptions.extend(value for name, value in locals().items() if name.startswith('option'))

        print(f"{interaction.user}: /choose {RawOptions}")

        while i < len(RawOptions):
            if RawOptions[i] != None:
                Options.append(RawOptions[i])
            
            i += 1

        chosen_option_int = random.randint(0, len(Options)-1)
        chosen_option = Options[chosen_option_int]

        await interaction.response.send_message(f"I have chosen `Option {chosen_option_int+1}`:\n{chosen_option}")

        uses_update("command_uses", "choose")

def setup(client):
    client.add_cog(choose(client))