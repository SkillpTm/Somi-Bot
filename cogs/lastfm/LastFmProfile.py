###package#import###############################################################################

import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
import requests

client = commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from cogs._global_data.global_data import network
from database.database_command_uses import uses_update
from database.database_lastfm import lastfm_get_user_from_db
from utilities.maincommands import checks
from utilities.variables import LASTFM_COLOR
from utilities.partial_commands import get_nick_else_name, embed_builder



class LastFmProfile(commands.Cog):

    def __init__(self, client):
        self.client = client

    from utilities.maincommands import lastfm

    ###lf#profile###########################################################

    @lastfm.subcommand(name = "profile", description = "shows stats about someone's LastFm account")
    async def profile(self,
                      interaction: Interaction,
                      *,
                      member: nextcord.Member = SlashOption(description="the user you want to know stats about", required=False)):
        if not checks(interaction):
            return

        if member == None:
            member = interaction.guild.get_member(interaction.user.id)

        print(f"{interaction.user}: /lf profile {member}")

        lastfm_username = lastfm_get_user_from_db(member.id)

        if not lastfm_username:
            await interaction.response.send_message(f"{member.mention} has not setup their LastFm account.", ephemeral=True)
            return

        request_url = f"http://ws.audioscrobbler.com/2.0/?method=user.getinfo&username={lastfm_username}&limit=1&api_key={network.api_key}&format=json"

        if not requests.get(request_url).status_code == 200:
            await interaction.response.send_message(f"The user `{lastfm_username}` couldn't be found on LastFm.", ephemeral=True)
            return

        profile_user_data = requests.get(request_url).json()
        name = get_nick_else_name(member)

        embed = embed_builder(title = f"LastFm User Information: `{name}`",
                              color = LASTFM_COLOR,
                              thumbnail = profile_user_data['user']['image'][3]['#text'],
                              footer = "DEFAULT_KST_FOOTER",

                              field_one_name = "LastFm name:",
                              field_one_value = f"[{profile_user_data['user']['name']}]({profile_user_data['user']['url']})",
                              field_one_inline = True,

                              field_two_name = "Plays:",
                              field_two_value = f"__**{profile_user_data['user']['playcount']}**__",
                              field_two_inline = True,

                              field_three_name = "Registered at:",
                              field_three_value = f"<t:{int(profile_user_data['user']['registered']['unixtime'])}>",
                              field_three_inline = False,
                                                
                              field_four_name = "Artists:",
                              field_four_value = profile_user_data['user']['artist_count'],
                              field_four_inline = True,
                                                
                              field_five_name = "Albums:",
                              field_five_value = profile_user_data['user']['album_count'],
                              field_five_inline = True,
                                                
                              field_six_name = "Tracks:",
                              field_six_value = profile_user_data['user']['track_count'],
                              field_six_inline = True)

        await interaction.response.send_message(embed=embed)

        uses_update("command_uses", "lf profile")



def setup(client):
    client.add_cog(LastFmProfile(client))