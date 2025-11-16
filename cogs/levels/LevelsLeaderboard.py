import nextcord
import nextcord.ext.commands as nextcord_C

from lib.database import db, Order
from lib.helpers import EmbedFunctions
from lib.managers import Commands, Config
from lib.modules import SomiBot



class LevelsLeaderboard(nextcord_C.Cog):

    from cogs.basic.ParentCommand import ParentCommand

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    @ParentCommand.levels.subcommand(
        Commands().data["levels leaderboard"].alias,
        Commands().data["levels leaderboard"].description,
        name_localizations = {country_tag: Commands().data["levels leaderboard"].name for country_tag in nextcord.Locale}
    )
    async def levels_leaderboard(self, interaction: nextcord.Interaction) -> None:
        """Displays the top 10 (or less, if there isn't 10 users in the levels table) users by XP"""

        await interaction.response.defer(with_message=True)

        output: str = ""
        rank: int = 1

        async for entry in db.Level._.get_multiple(
            [db.Level.USER, db.Level.XP],
            {db.Level.SERVER: interaction.guild.id},
            db.Level.XP,
            Order.DESCENDING,
            10
        ):
            name = f"[Deleted User] - ({db.Level.USER.retrieve(entry)})" # default value for, if the user's account doesn't exit anymore

            # check if the user is still in the server
            if (member := interaction.guild.get_member(db.Level.USER.retrieve(entry))):
                name = member.mention
            # check if the user's account still exists
            elif not member and (user := self.client.get_user(db.Level.USER.retrieve(entry))):
                name = user.display_name

            output += f"**{rank}. {name}** - Level: __`{db.Level._.get_level(db.Level.XP.retrieve(entry))}`__\n"
            rank += 1

        output = output or "`No users have earned any XP on this server yet.`"

        server_icon_url = interaction.guild.icon.url if interaction.guild.icon else Config().DEFAULT_PFP

        embed = EmbedFunctions().builder(
            color = Config().BOT_COLOR,
            thumbnail = server_icon_url,
            title = f"`{interaction.guild.name}`: Top users by level",
            description = output
        )

        await interaction.followup.send(embed=embed)



def setup(client: SomiBot) -> None:
    client.add_cog(LevelsLeaderboard(client))