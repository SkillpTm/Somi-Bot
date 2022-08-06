###package#import###############################################################################

import nextcord
from nextcord import Embed, Interaction, SlashOption
from nextcord.ext import commands

client = commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from utilities.maincommands import checks
from utilities.partial_commands import embed_kst_footer, embed_set_thumbnail, embed_get_title_name, embed_get_userinfo



class userinfo(commands.Cog):

    def __init__(self, client):
        self.client = client

    ###userinfo###########################################################

    @nextcord.slash_command(name="userinfo", description = "gives information about a user")
    async def userinfo(self,
                       interaction: Interaction,
                       *,
                       member: nextcord.Member = SlashOption(description="The user you want the information about (nothing=yourself)", required=False)):
        if not checks(interaction):
            return

        print(f"{interaction.user}: /userinfo {member}")

        if member == None:
            member = interaction.guild.get_member(interaction.user.id)

        title_name = embed_get_title_name(member)

        embed = Embed(title = f"User Information: `{title_name}`",
                      colour=member.color)
        embed_kst_footer(embed)
        embed_set_thumbnail(member, embed)
        embed_get_userinfo(member, embed)

        await interaction.send(embed=embed)

        uses_update("command_uses", "userinfo")

    ###userinfo#alias###########################################################

    @nextcord.slash_command(name="ui", description = "gives information about a user (alias of /userinfo)")
    async def ui(self,
                 interaction: Interaction,
                 *,
                 member: nextcord.Member = SlashOption(description="The user you want the information about (nothing=yourself)", required=False)):
        if not checks(interaction):
            return

        print(f"{interaction.user}: /ui {member}")

        if member == None:
            member = interaction.guild.get_member(interaction.user.id)

        title_name = embed_get_title_name(member)

        embed = Embed(title = f"User Information: `{title_name}`",
                      colour=member.color)
        embed_kst_footer(embed)
        embed_set_thumbnail(member, embed)
        embed_get_userinfo(member, embed)

        await interaction.send(embed=embed)

        uses_update("command_uses", "ui")

def setup(client):
    client.add_cog(userinfo(client))