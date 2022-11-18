###package#import###############################################################################

import nextcord

client = nextcord.ext.commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from database.database_levels import check_level_for_server_and_user, get_user_level, get_all_user_levels
from utilities.maincommands import checks
from utilities.partial_commands import embed_builder, get_nick_else_name, get_user_avatar
from utilities.variables import BOT_COLOR



class LevelsRank(nextcord.ext.commands.Cog):

    def __init__(self, client):
        self.client = client

    from utilities.maincommands import levels

    ###level#roles#add###########################################################

    @levels.subcommand(name = "rank", description = "shows your rank and level on this server")
    async def levels_rank(self,
                          interaction: nextcord.Interaction,
                          *,
                          member: nextcord.Member = nextcord.SlashOption(description="the member you want to see the rank of", required=False)):
        if not checks(self.client, interaction.guild, interaction.user):
            return

        if member == None:
            member = interaction.guild.get_member(interaction.user.id)

        print(f"{interaction.user}: /levels rank {member}")

        await interaction.response.defer(with_message=True)

        check_level_for_server_and_user(member.guild.id, member.id)

        user_level, xp_until_next_level = get_user_level(interaction.guild.id, member.id)

        next_level_xp = (user_level-1) * 200 + 300
        
        percent_left: float = 20 * (float(xp_until_next_level) / float(next_level_xp))
        percent_bar: str = "[" + "█" * (20 - (int(percent_left))) + " -" * int(percent_left) + "]"

        user_ids_and_levels = get_all_user_levels(interaction.guild.id)

        for index, user in enumerate(user_ids_and_levels):
            if member.id == user[0]:
                rank = index + 1
                break

        output_percentage = int((1 - (float(xp_until_next_level) / float(next_level_xp))) * 100)

        if user_level == 0:
            xp_until_next_level = 0
            next_level_xp = 0
            output_percentage = 100

        name = get_nick_else_name(member)
        member_avatar_url = get_user_avatar(member)

        embed = embed_builder(title = f"Stats for `{name}` on `{interaction.guild.name}`",
                              color = BOT_COLOR,
                              thumbnail = member_avatar_url,
                              footer = "DEFAULT_KST_FOOTER",

                              field_one_name = "Level:",
                              field_one_value = f"`{user_level}`",
                              field_one_inline = True,
                                                
                              field_two_name = "Rank",
                              field_two_value = f"`{rank}`",
                              field_two_inline = True,
                              
                              field_three_name = "Level Progress:",
                              field_three_value = f"{percent_bar}\n{next_level_xp - xp_until_next_level}/{next_level_xp} ({output_percentage}%)",
                              field_three_inline = False)

        await interaction.followup.send(embed=embed)

        uses_update("command_uses", "levels rank")



def setup(client):
    client.add_cog(LevelsRank(client))