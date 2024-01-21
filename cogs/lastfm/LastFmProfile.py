####################################################################################################

import nextcord
import nextcord.ext.commands as nextcord_C
import nextcord.ext.application_checks as nextcord_AC
import requests
import time

####################################################################################################

from lib.db_modules import LastFmDB
from lib.modules import Checks, EmbedFunctions, Get
from lib.utilities import SomiBot



class LastFmProfile(nextcord_C.Cog):

    def __init__(self, client):
        self.client: SomiBot = client

    from lib.utilities.main_commands import lastfm

    ####################################################################################################

    @lastfm.subcommand(name = "profile", description = "shows stats about someone's LastFm account")
    @nextcord_AC.check(Checks().interaction_in_guild())
    async def lastfm_profile(self,
                             interaction: nextcord.Interaction,
                             *,
                             member: nextcord.Member = nextcord.SlashOption(description="the user you want to know stats about", required=False)):
        """This command outputs information about a user's lastfm account"""

        if not member:
            member = interaction.guild.get_member(interaction.user.id)

        self.client.Loggers.action_log(f"Guild: {interaction.guild.id} ~ Channel: {interaction.channel.id} ~ User: {interaction.user.id} ~ /lf profile {member.id}")

        lastfm_username = LastFmDB().get(member.id)

        if not lastfm_username:
            await interaction.response.send_message(embed=EmbedFunctions().error(f"{member.mention} has not setup their LastFm account.\nTo setup a LastFm account use `/lf set`."), ephemeral=True)
            return

        await interaction.response.defer(with_message = True)

        request_url = requests.get(f"http://ws.audioscrobbler.com/2.0/?method=user.getinfo&username={lastfm_username}&limit=1&api_key={self.client.Keychain.LAST_FM_API_KEY}&format=json")

        if not request_url.status_code == 200:
            await interaction.followup.send(embed=EmbedFunctions().error("LastFm didn't respond correctly, try in a few minutes again!"))
            return

        profile_user_data = request_url.json()

        if profile_user_data['user']['image'][3]['#text']:
            lastfm_user_pfp = profile_user_data['user']['image'][3]['#text']
        else:
            lastfm_user_pfp = self.client.DEFAULT_PFP
            
        days_plays_ratio: float = round(int(profile_user_data['user']['playcount']) / (int((int(time.time()) - int(profile_user_data['user']['registered']['unixtime'])) / 60 / 60 / 24)), 2)

        embed = EmbedFunctions().builder(
            color = self.client.LASTFM_COLOR,
            thumbnail = lastfm_user_pfp,
            author = f"{member.display_name} LastFm User Data",
            author_icon = self.client.LASTFM_ICON,
            footer = "DEFAULT_KST_FOOTER",
            fields = [
                [
                    "LastFm name:",
                    f"[{Get().markdown_safe(profile_user_data['user']['name'])}]({profile_user_data['user']['url']})",
                    True
                ],

                [
                    "Total Plays:",
                    f"__**{profile_user_data['user']['playcount']}**__",
                    True
                ],

                [
                    "Average Plays/Day:",
                    f"{days_plays_ratio}",
                    True
                ],

                [
                    "Registered at:",
                    f"<t:{int(profile_user_data['user']['registered']['unixtime'])}>",
                    False
                ],

                [
                    "Unique Artists:",
                    profile_user_data['user']['artist_count'],
                    True
                ],

                [
                    "Unique Albums:",
                    profile_user_data['user']['album_count'],
                    True
                ],

                [
                    "Unique Tracks:",
                    profile_user_data['user']['track_count'],
                    True
                ]
            ]
        )

        await interaction.followup.send(embed=embed)



def setup(client: SomiBot):
    client.add_cog(LastFmProfile(client))