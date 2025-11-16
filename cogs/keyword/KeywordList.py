import nextcord
import nextcord.ext.commands as nextcord_C

from lib.database import db, Order
from lib.helpers import EmbedFunctions
from lib.managers import Commands, Config
from lib.modules import SomiBot



class KeywordList(nextcord_C.Cog):

    from cogs.basic.ParentCommand import ParentCommand

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    @ParentCommand.keyword.subcommand(Commands().data["keyword list"].name, Commands().data["keyword list"].description)
    async def keyword_list(self, interaction: nextcord.Interaction) -> None:
        """This command outputs a list of all keywords a user has"""

        await interaction.response.defer(ephemeral=True, with_message=True)
        user_keywords: list[str]

        if not (user_keywords := await db.Keyword.KEYWORD.get_all(where={db.Keyword.SERVER: interaction.guild.id, db.Keyword.USER: interaction.user.id}, order_by=db.Keyword.KEYWORD, order=Order.ASCENDING)):
            await interaction.followup.send(embed=EmbedFunctions().get_error_message("You don't have any keywords.\nTo add a keyword use `/keyword add`."), ephemeral=True)
            return

        output = ""

        for index, keyword in enumerate(user_keywords):
            output += f"{index + 1}. `{keyword}`\n"

        embed = EmbedFunctions().builder(
            color = Config().BOT_COLOR,
            author = f"Keyword List for: {interaction.user.display_name}",
            author_icon = interaction.user.display_avatar.url,
            fields = [
                [
                    "Keywords:",
                    output,
                    True
                ]
            ]
        )

        await interaction.followup.send(embed=embed, ephemeral=True)



def setup(client: SomiBot) -> None:
    client.add_cog(KeywordList(client))