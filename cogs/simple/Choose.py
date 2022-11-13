###package#import###############################################################################

import nextcord
import random

client = nextcord.ext.commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from utilities.maincommands import checks



class Choose(nextcord.ext.commands.Cog):

    def __init__(self, client):
        self.client = client

    ###choose###########################################################
    
    @nextcord.slash_command(name = "choose", description = "let the bot choose one of the options for you!")
    async def choose(self,
                     interaction: nextcord.Interaction,
                     *,
                     option1: str = nextcord.SlashOption(description="first option", required=True, min_length=1, max_length=200),
                     option2: str = nextcord.SlashOption(description="second option", required=True, min_length=1, max_length=200),
                     option3: str = nextcord.SlashOption(description="third option", required=False, min_length=1, max_length=200),
                     option4: str = nextcord.SlashOption(description="fourth option", required=False, min_length=1, max_length=200),
                     option5: str = nextcord.SlashOption(description="fifth option", required=False, min_length=1, max_length=200),
                     option6: str = nextcord.SlashOption(description="sixth option", required=False, min_length=1, max_length=200),
                     option7: str = nextcord.SlashOption(description="seventh option", required=False, min_length=1, max_length=200),
                     option8: str = nextcord.SlashOption(description="eigth option", required=False, min_length=1, max_length=200),
                     option9: str = nextcord.SlashOption(description="ninth option", required=False, min_length=1, max_length=200),
                     option10: str = nextcord.SlashOption(description="tenth option", required=False, min_length=1, max_length=200)):
        if not checks(interaction.guild, interaction.user):
            return

        RawOptions = []
        RawOptions.extend(value for name, value in locals().items() if name.startswith('option'))

        print(f"{interaction.user}: /choose {RawOptions}")

        Options = [option for option in RawOptions if option != None]

        chosen_option_int = random.randint(0, len(Options)-1)
        chosen_option = Options[chosen_option_int]

        await interaction.response.send_message(f"I have chosen __Option {chosen_option_int+1}__:\n`{chosen_option}`")

        uses_update("command_uses", "choose")



def setup(client):
    client.add_cog(Choose(client))