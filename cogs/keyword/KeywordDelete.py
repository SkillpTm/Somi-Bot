import typing

import nextcord
import nextcord.ext.commands as nextcord_C

from cogs.basic.ParentCommand import ParentCommand
from lib.database import db, Order
from lib.helpers import EmbedFunctions, Get
from lib.managers import Commands
from lib.modules import SomiBot, YesNoButtons



class KeywordDelete(nextcord_C.Cog):

    def __init__(self, client: SomiBot) -> None:
        self.client = client


    @ParentCommand.keyword.subcommand(Commands().data["keyword delete"].name, Commands().data["keyword delete"].description)
    async def keyword_delete(
        self,
        interaction: nextcord.Interaction[SomiBot],
        *,
        keyword: str = nextcord.SlashOption(
            Commands().data["keyword delete"].parameters["keyword"].name,
            Commands().data["keyword delete"].parameters["keyword"].description,
            required = True,
            min_length = 2,
            max_length = 50
        ),
        delete_all: typing.Literal["Yes", ""] = nextcord.SlashOption(
            Commands().data["keyword delete"].parameters["delete_all"].name,
            Commands().data["keyword delete"].parameters["delete_all"].description,
            required = False,
            choices = ["Yes"],
            min_length = 2,
            max_length = 50,
            default = ""
        )
    ) -> None:
        """This command let's you delete a keyword by it's name or all keywords with 'ALL'"""

        await interaction.response.defer(ephemeral=True, with_message=True)

        if not keyword and not delete_all:
            await interaction.send(embed=EmbedFunctions().get_error_message("Please either provide a keyword or choose to delete all your keywords."))
            return

        if not await db.Keyword._.get_all(where={db.Keyword.SERVER: interaction.guild.id, db.Keyword.USER: interaction.user.id}):
            await interaction.send(embed=EmbedFunctions().get_error_message("You don't have any keywords.\nTo add a keyword use `/keyword add`."))
            return

        if delete_all == "Yes":
            await self.delete_all(interaction)
            return

        keyword = keyword.lower()

        if not await db.Keyword._.delete(where={db.Keyword.SERVER: interaction.guild.id, db.Keyword.USER: interaction.user.id, db.Keyword.KEYWORD: keyword}):
            await interaction.send(embed=EmbedFunctions().get_error_message(f"You don't have a keyword called `{keyword}`.\nTo get a list of your keywords use `/keyword list`."))
            return

        await interaction.send(embed=EmbedFunctions().get_success_message(f"`{keyword}` has been deleted from your keywords."))


    async def delete_all(self, interaction: nextcord.Interaction[SomiBot]) -> None:
        """asks the user if they want to delete all their keywords and does as answered"""

        view = YesNoButtons(interaction=interaction) # type: ignore
        await interaction.send(embed=EmbedFunctions().get_info_message("Do you really want to delete **ALL** your keywords __**(they can't be recovered)**__?"), view=view)
        await view.wait()

        if not view.value:
            await interaction.send(embed=EmbedFunctions().get_error_message("Your keywords have **not** been deleted!"))
            return

        await db.Keyword._.delete(where={db.Keyword.SERVER: interaction.guild.id, db.Keyword.USER: interaction.user.id}, limit=1_000_000)

        await interaction.send(embed=EmbedFunctions().get_success_message("**ALL** your keywords have been deleted!"))


    @keyword_delete.on_autocomplete("keyword")
    async def keyword_delete_autocomplete_keyword(
        self,
        interaction: nextcord.Interaction[SomiBot],
        keyword: str
    ) -> None:
        """provides autocomplete suggestions to discord"""

        await interaction.response.send_autocomplete(
            Get.autocomplete(
                keyword,
                typing.cast(list[str], await db.Keyword.KEYWORD.get_all(where={db.Keyword.SERVER: interaction.guild.id, db.Keyword.USER: interaction.user.id}, order_by=db.Keyword.KEYWORD, order=Order.ASCENDING))
            )
        )



def setup(client: SomiBot) -> None:
    client.add_cog(KeywordDelete(client))