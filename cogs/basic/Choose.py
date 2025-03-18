import nextcord
import nextcord.ext.commands as nextcord_C
import random

from lib.modules import EmbedFunctions, Get
from lib.utilities import OptionsButton, SomiBot



class Choose(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################
    
    @nextcord.slash_command(
        name = "select",
        description = "let the bot choose one of the options for you!",
        name_localizations = {country_tag:"choose" for country_tag in nextcord.Locale}
    )
    async def choose(
        self,
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
        option10: str = nextcord.SlashOption(description="tenth option", required=False, min_length=1, max_length=200)
    ) -> None:
        """This command randomly chooses between one of the select 2-10 options"""

        options: dict[str, str] = {}

        # get all the options that got actually filled in
        for name, value in locals().items():
            if name.startswith("option") and value and value != options:
                options[name] = value


        self.client.Loggers.action_log(Get.log_message(
            interaction,
            "/choose",
            options
        ))

        await interaction.response.defer(with_message=True)

        chosen_key = random.choice(list(options))


        view = OptionsButton(interaction=interaction)
        await interaction.followup.send(f"I have chosen __Option {chosen_key[-1]}__:\n`{options[chosen_key]}`", view=view)
        await view.wait()

        # if the button to see all options not pressed return early
        if not view.value:
            return

        AllOptionsOutput = ""

        for name, value in options.items():
            # if the option is the chosen option underscore it
            if name == chosen_key:
                AllOptionsOutput += f"__**Option {name[-1]}: {value}**__\n"
                continue

            AllOptionsOutput += f"Option {name[-1]}: {value}\n"

        await interaction.followup.send(embed=EmbedFunctions().get_info_message(AllOptionsOutput, self.client)) 



def setup(client: SomiBot) -> None:
    client.add_cog(Choose(client))