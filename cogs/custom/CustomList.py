import math
import typing

import nextcord
import nextcord.ext.commands as nextcord_C

from lib.database import db, Order
from lib.helpers import EmbedFunctions
from lib.managers import Commands, Config
from lib.modules import PageButtons, SomiBot



class CustomList(nextcord_C.Cog):

    def __init__(self, client: SomiBot) -> None:
        self.client = client


    @nextcord.slash_command(
        Commands().data["custom-list"].alias,
        Commands().data["custom-list"].description,
        name_localizations = {country_tag: Commands().data["custom-list"].name for country_tag in nextcord.Locale},
        integration_types = [nextcord.IntegrationType.guild_install],
        contexts = [nextcord.InteractionContextType.guild]
    )
    async def custom_list(self, interaction: nextcord.Interaction[SomiBot]) -> None:
        """This command provides a list of all custom-commands of a guild"""

        await interaction.response.defer(ephemeral=True, with_message=True)

        if not (all_commandnames := typing.cast(list[dict[str, str]], await db.CustomCommand._.get_all(
            [db.CustomCommand.NAME, db.CustomCommand.TEXT],
            {db.CustomCommand.SERVER: interaction.guild.id},
            db.CustomCommand.NAME,
            Order.ASCENDING)
        )):
            await interaction.followup.send(embed=EmbedFunctions().get_error_message("There are no custom-commands on this server.\nTo add a custom-command use `/custom add`."))
            return

        await self.custom_list_rec(interaction, all_commandnames, 1)


    async def custom_list_rec(self, interaction: nextcord.Interaction[SomiBot], all_commandnames: list[dict[str, str]], page: int) -> None:
        """This function is used to paginate through the custom-command list"""

        output: list[str] = []

        for index, entry in enumerate(all_commandnames[10*(page-1):]):
            if len(output) >= 10:
                break

            text = str(db.CustomCommand.TEXT.retrieve(entry))
            text = f"{text[:100]}..." if len(text) > 100 else text

            output.append(f"`{index+1 + 10*(page-1)}.` /cc [{db.CustomCommand.NAME.retrieve(entry)}]: {text}")

        embed = EmbedFunctions().builder(
            color = Config().BOT_COLOR,
            author = f"Custom Commands on {interaction.guild.name}",
            author_icon = interaction.guild.icon.url if interaction.guild.icon else Config().DEFAULT_PFP,
            description = "\n".join(output)
        )

        view = PageButtons(page, math.ceil(len(all_commandnames)/10), interaction) # type: ignore

        await interaction.edit_original_message(embed=embed, view=view)
        await view.update_buttons()
        await view.wait()

        if not view.value:
            return

        await self.custom_list_rec(interaction, all_commandnames, view.page)



def setup(client: SomiBot) -> None:
    client.add_cog(CustomList(client))