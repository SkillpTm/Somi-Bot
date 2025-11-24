import re

import nextcord
import nextcord.ext.commands as nextcord_C

from cogs.basic.ParentCommand import ParentCommand
from lib.database import db
from lib.helpers import EmbedFunctions
from lib.managers import Commands
from lib.modules import SomiBot



class KeywordAdd(nextcord_C.Cog):

    def __init__(self, client: SomiBot) -> None:
        self.client = client


    @ParentCommand.keyword.subcommand(Commands().data["keyword add"].name, Commands().data["keyword add"].description)
    async def keyword_add(
        self,
        interaction: nextcord.Interaction[SomiBot],
        *,
        keyword: str = nextcord.SlashOption(
            Commands().data["keyword add"].parameters["keyword"].name,
            Commands().data["keyword add"].parameters["keyword"].description,
            required = True,
            min_length = 2,
            max_length = 50
        )
    ) -> None:
        """This command adds a global keyword to the bot for a user"""

        await interaction.response.defer(ephemeral=True, with_message=True)

        keyword = keyword.lower()

        # make sure keywords are only letters and numbers
        if not re.match(r"^[a-z0-9]+$", keyword):
            await interaction.send(embed=EmbedFunctions().get_error_message("You can only have letters and numbers in your keywords!"))
            return

        added = await db.Keyword._.add_unique(
            {db.Keyword.KEYWORD: keyword, db.Keyword.SERVER: interaction.guild.id, db.Keyword.USER: interaction.user.id},
            {db.Keyword.KEYWORD: keyword, db.Keyword.SERVER: interaction.guild.id, db.Keyword.USER: interaction.user.id}
        )

        if not added:
            await interaction.send(embed=EmbedFunctions().get_error_message(f"You already have `{keyword}` as a keyword.\nTo get a list of your keywords use `/keyword list`."))
            return

        await interaction.send(embed=EmbedFunctions().get_success_message(f"`{keyword}` has been added to your keywords."))



def setup(client: SomiBot) -> None:
    client.add_cog(KeywordAdd(client))