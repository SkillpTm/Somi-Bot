###package#import###############################################################################

import nextcord
import nextcord.ext.commands

client = nextcord.ext.commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from database.database_levels import get_all_user_levels
from utilities.maincommands import checks
from utilities.partial_commands import embed_builder, get_nick_else_name
from utilities.variables import BOT_COLOR, DEFAULT_PFP



class LevelsLeaderboard(nextcord.ext.commands.Cog):

    def __init__(self, client):
        self.client: nextcord.ext.commands.Bot = client

    from utilities.maincommands import levels

    ###level#roles#add###########################################################

    @levels.subcommand(name = "leaderboard", description = "shows the top10 users by level of this server")
    async def levels_leaderboard(self,
                                 interaction: nextcord.Interaction):
        if not checks(self.client, interaction.guild, interaction.user):
            return

        print(f"{interaction.user}: /levels leaderboard")

        await interaction.response.defer(with_message=True)

        user_ids_and_levels = get_all_user_levels(interaction.guild.id)
        counter: int = 0
        output: str = ""
        print(len(user_ids_and_levels))

        while counter < len(user_ids_and_levels):
            for index, user in enumerate(user_ids_and_levels):
                try:
                    member = interaction.guild.get_member(user[0])
                except:
                    member = self.client.get_user(user[0])

                name = get_nick_else_name(member)

                output += f"**{index+1}. {name}**\nLevel: `{user[1]}`\n\n"

                counter += 1

            if counter > 10:
                break

        if interaction.guild.icon is not None:
            server_icon_url = interaction.guild.icon
        else:
            server_icon_url = DEFAULT_PFP

        embed = embed_builder(title = f"Top users by level for `{interaction.guild.name}`",
                              color = BOT_COLOR,
                              description = output,
                              thumbnail = server_icon_url,
                              footer = "DEFAULT_KST_FOOTER")

        await interaction.followup.send(embed=embed)

        uses_update("command_uses", "levels rank")



def setup(client):
    client.add_cog(LevelsLeaderboard(client))