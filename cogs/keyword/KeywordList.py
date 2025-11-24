import math
import typing

import nextcord
import nextcord.ext.commands as nextcord_C

from cogs.basic.ParentCommand import ParentCommand
from lib.database import db, Order
from lib.helpers import EmbedFunctions
from lib.managers import Commands, Config
from lib.modules import PageButtons, SomiBot



class KeywordList(nextcord_C.Cog):

    def __init__(self, client: SomiBot) -> None:
        self.client = client


    @ParentCommand.keyword.subcommand(Commands().data["keyword list"].name, Commands().data["keyword list"].description)
    async def keyword_list(self, interaction: nextcord.Interaction[SomiBot]) -> None:
        """This command outputs a list of all keywords a user has"""

        await interaction.response.defer(ephemeral=True, with_message=True)

        if not (all_keywords := typing.cast(list[dict[str, str]], await db.Keyword.KEYWORD.get_all(
            where = {db.Keyword.SERVER: interaction.guild.id, db.Keyword.USER: interaction.user.id},
            order_by = db.Keyword.KEYWORD,
            order = Order.ASCENDING)
        )):
            await interaction.followup.send(embed=EmbedFunctions().get_error_message("You don't have any keywords.\nTo add a keyword use `/keyword add`."))
            return

        await self.keyword_list_rec(interaction, all_keywords, 1)


    async def keyword_list_rec(self, interaction: nextcord.Interaction[SomiBot], all_keywords: list[dict[str, str]], page: int) -> None:
        """This function is used to paginate through the keyword list"""

        output: list[str] = []

        for index, entry in enumerate(all_keywords[10*(page-1):]):
            if len(output) >= 10:
                break

            output.append(f"`{index+1 + 10*(page-1)}.` {db.Keyword.KEYWORD.retrieve(entry)}")

        embed = EmbedFunctions().builder(
            color = Config().BOT_COLOR,
            author = f"Keywords for {interaction.user.display_name}",
            author_icon = interaction.user.display_avatar.url,
            description = "\n".join(output)
        )

        view = PageButtons(page, math.ceil(len(all_keywords)/10), interaction) # type: ignore

        await interaction.edit_original_message(embed=embed, view=view)
        await view.update_buttons()
        await view.wait()

        if not view.value:
            return

        await self.keyword_list_rec(interaction, all_keywords, view.page)



def setup(client: SomiBot) -> None:
    client.add_cog(KeywordList(client))