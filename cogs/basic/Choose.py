import random
import typing

import nextcord
import nextcord.ext.commands as nextcord_C

from lib.helpers import EmbedFunctions
from lib.managers import Commands, Config, Logger
from lib.modules import OptionsButton, SomiBot



class ChooseModal(nextcord.ui.Modal):

    def __init__(self, client: SomiBot) -> None:
        super().__init__("Make Somi choose for you!", timeout=None)
        self.client = client

        self.choice_text: nextcord.ui.TextInput[typing.Any] = nextcord.ui.TextInput(
            label = "What do you need a choice for?",
            style = nextcord.TextInputStyle.short,
            min_length = 1,
            max_length = 250,
            required = False
        )

        self.choose: nextcord.ui.TextInput[typing.Any] = nextcord.ui.TextInput(
            label = "Options:",
            style = nextcord.TextInputStyle.paragraph,
            min_length = 1,
            max_length = 4000,
            placeholder = "each new line is a new option",
            required = True
        )

        self.add_item(self.choice_text)
        self.add_item(self.choose)


    async def callback(self, interaction: nextcord.Interaction[SomiBot]) -> None:
        """chooses an option and displays it"""

        options: dict[str, str] = {}

        if not self.choose.value:
            return

        # seperate options by new lines
        for option in self.choose.value.split("\n"):
            if option.strip():
                options[f"{len(options)+1}"] = option.strip()

        Logger().action_log(interaction, "/choose", options) # type: ignore

        chosen_key = random.choice(list(options.keys()))

        choice_text = f"```{self.choice_text.value}```" if self.choice_text.value else ""

        view = OptionsButton(interaction=interaction) # type: ignore
        await interaction.send(f"{choice_text}I have chosen __Option {chosen_key}__:\n`{options[chosen_key]}`", view=view)
        await view.wait()

        # if the button to see all options isn't pressed return early
        if not view.value:
            return

        output = ""

        for name, value in options.items():
            # if the option is the chosen option underscore it
            if name == chosen_key:
                output += f"__**Option {name[-1]}: {value}**__\n"
                continue

            output += f"Option {name[-1]}: {value}\n"

        embed = EmbedFunctions.builder(
            color = Config().BOT_COLOR,
            title = choice_text.strip(),
            description = output
        )

        await interaction.send(embed=embed)



class Choose(nextcord_C.Cog):

    def __init__(self, client: SomiBot) -> None:
        self.client = client


    @nextcord.slash_command(
        Commands().data["choose"].alias,
        Commands().data["choose"].description,
        name_localizations = {country_tag: Commands().data["choose"].name for country_tag in nextcord.Locale},
        integration_types=[
            nextcord.IntegrationType.user_install,
            nextcord.IntegrationType.guild_install,
        ],
        contexts=[
            nextcord.InteractionContextType.guild,
            nextcord.InteractionContextType.bot_dm,
            nextcord.InteractionContextType.private_channel,
        ]
    )
    async def choose(self, interaction: nextcord.Interaction[SomiBot]) -> None:
        """This command randomly chooses between any of the options"""

        await interaction.response.send_modal(ChooseModal(self.client))



def setup(client: SomiBot) -> None:
    client.add_cog(Choose(client))