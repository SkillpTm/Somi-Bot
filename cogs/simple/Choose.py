####################################################################################################

import nextcord
import nextcord.ext.commands as nextcord_C
import nextcord.ext.application_checks as nextcord_AC
import random

####################################################################################################

from lib.modules import Checks, EmbedFunctions
from lib.utilities import OptionsButton, SomiBot



class Choose(nextcord_C.Cog):

    def __init__(self, client):
        self.client: SomiBot = client

    ####################################################################################################
    
    @nextcord.slash_command(name = "select", description = "let the bot choose one of the options for you!", name_localizations = {country_tag:"choose" for country_tag in nextcord.Locale})
    @nextcord_AC.check(Checks().interaction_in_guild())
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
        """This command randomly chooses between one of the select 2-10 options"""

        options = [[value, name] for name, value in locals().items() if name.startswith('option') and value != None]

        self.client.Loggers.action_log(f"Guild: {interaction.guild.id} ~ Channel: {interaction.channel.id} ~ User: {interaction.user.id} ~ /choose {options}")

        await interaction.response.defer(with_message=True)

        chosen_option = random.choice(options)


        view = OptionsButton(interaction=interaction)
        await interaction.followup.send(f"I have chosen __Option {chosen_option[1][int(len(chosen_option[1])-1)]}__:\n`{chosen_option[0]}`", view=view)
        await view.wait()

        if view.value:

            output = ""

            for option in options:
                if option != chosen_option:
                    output += f"Option {option[1][int(len(option[1])-1)]}: {option[0]}\n"
                else:
                    output += f"__**Option {option[1][int(len(option[1])-1)]}: {option[0]}**__\n"

            await interaction.followup.send(embed=EmbedFunctions().info_message(output, self.client)) 



def setup(client: SomiBot):
    client.add_cog(Choose(client))