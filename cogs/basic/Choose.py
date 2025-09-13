import nextcord
import nextcord.ext.commands as nextcord_C
import random

from lib.modules import EmbedFunctions, Get
from lib.utilities import OptionsButton, SomiBot



class ChooseModal(nextcord.ui.Modal):

    def __init__(self, client) -> None:
        super().__init__("Let Somi choose between something!", timeout=None)
        self.client: SomiBot = client

        self.choose = nextcord.ui.TextInput(
            label = "Options:",
            style = nextcord.TextInputStyle.paragraph,
            min_length = 1,
            max_length = 4000,
            placeholder = "a new line represents a new option",
            required = True
        )

        self.add_item(self.choose)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        """chooses an option and displays it"""

        options: dict[str, str] = {}

        # seperate options by new lines
        for index, option in enumerate(self.choose.value.split("\n")):
            options[f"{index+1}"] = option

        self.client.Loggers.action_log(Get.log_message(
            interaction,
            "/choose",
            options
        ))

        chosen_key = random.choice(list(options.keys()))


        view = OptionsButton(interaction=interaction)
        await interaction.response.send_message(f"I have chosen __Option {chosen_key}__:\n`{options[chosen_key]}`", view=view)
        await view.wait()

        # if the button to see all options isn't pressed return early
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



class Choose(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    @nextcord.slash_command(
        name = "select",
        description = "let the bot choose one of the options for you!",
        name_localizations = {country_tag:"choose" for country_tag in nextcord.Locale}
    )
    async def choose(self, interaction: nextcord.Interaction) -> None:
        """This command randomly chooses between any of the options"""

        self.client.Loggers.action_log(Get.log_message(interaction, "/choose"))

        modal = ChooseModal(self.client)
        await interaction.response.send_modal(modal=modal)



def setup(client: SomiBot) -> None:
    client.add_cog(Choose(client))