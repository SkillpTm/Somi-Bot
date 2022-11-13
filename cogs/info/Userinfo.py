###package#import###############################################################################

import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands

client = commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from database.database_command_uses import uses_update
from utilities.maincommands import checks
from utilities.partial_commands import get_userinfo_embed



class userinfo(commands.Cog):

    def __init__(self, client):
        self.client = client

    ###userinfo###########################################################

    @nextcord.slash_command(name="userinfo", description = "gives information about a user")
    async def userinfo(self,
                       interaction: Interaction,
                       *,
                       member: nextcord.Member = SlashOption(description="the user you want the information about (nothing=yourself)", required=False)):
        if not checks(interaction):
            return

        print(f"{interaction.user}: /userinfo {member}")

        if member == None:
            member = interaction.guild.get_member(interaction.user.id)

        embed = get_userinfo_embed(member)

        await interaction.send(embed=embed)

        uses_update("command_uses", "userinfo")

    ###userinfo#alias###########################################################

    @nextcord.slash_command(name="ui", description = "gives information about a user (alias of /userinfo)")
    async def ui(self,
                 interaction: Interaction,
                 *,
                 member: nextcord.Member = SlashOption(description="the user you want the information about (nothing=yourself)", required=False)):
        if not checks(interaction):
            return

        print(f"{interaction.user}: /ui {member}")

        if member == None:
            member = interaction.guild.get_member(interaction.user.id)

        embed = get_userinfo_embed(member)

        await interaction.send(embed=embed)

        uses_update("command_uses", "ui")

def setup(client):
    client.add_cog(userinfo(client))