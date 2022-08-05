###package#import###############################################################################

import nextcord
from nextcord import Embed, Interaction, SlashOption
from nextcord.ext import commands

client = commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from utilities.maincommands import checks
from utilities.partial_commands import embed_kst_footer, embed_get_title_name
from utilities.variables import BOT_COLOR



class avatar(commands.Cog):

    def __init__(self, client):
        self.client = client

    ###avatar###########################################################

    @nextcord.slash_command(name="avatar", description = "posts someone's avatar")
    async def avatar(self,
                     interaction: Interaction,
                     *,
                     member: nextcord.Member = SlashOption(description="The user you want the avatar from (nothing=yourself)", required=False)):
        if not checks(interaction):
            return

        print(f"{interaction.user}: /avatar {member}")

        if member == None:
            member = interaction.guild.get_member(interaction.user.id)
        
        if member.avatar is not None:
            member_avatar = member.avatar
        else:
            member_avatar = member.default_avatar

        title_name = embed_get_title_name(member)

        embed = Embed(title = f"Avatar of: `{title_name}`",
                      url = member_avatar,
                      colour=BOT_COLOR)
        embed_kst_footer(embed)

        embed.set_image(url=member_avatar)

        await interaction.send(embed=embed)

        uses_update("command_uses", "avatar")

def setup(client):
    client.add_cog(avatar(client))