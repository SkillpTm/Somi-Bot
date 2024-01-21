####################################################################################################

import nextcord
import nextcord.ext.commands as nextcord_C
import nextcord.ext.application_checks as nextcord_AC
import requests
import urllib.parse

####################################################################################################

from lib.db_modules import LastFmDB
from lib.modules import Checks, EmbedFunctions, Get
from lib.utilities import SomiBot



class LastFmNowPlaying(nextcord_C.Cog):

    def __init__(self, client):
        self.client: SomiBot = client

    from lib.utilities.main_commands import lastfm

    ####################################################################################################

    @lastfm.subcommand(name = "nowplaying", description = "shows what someone is listening to right now", name_localizations = {country_tag:"np" for country_tag in nextcord.Locale})
    @nextcord_AC.check(Checks().interaction_in_guild())
    async def lastfm_now_playing(self,
                                 interaction: nextcord.Interaction,
                                 *,
                                 member: nextcord.Member = nextcord.SlashOption(description="the user you want to be shown, what they're listening to", required=False)):
        """This command displays what someone last listend to (and what they're listening to right now)"""

        if not member:
            member = interaction.guild.get_member(interaction.user.id)

        self.client.Loggers.action_log(f"Guild: {interaction.guild.id} ~ Channel: {interaction.channel.id} ~ User: {interaction.user.id} ~ /lf np {member.id}")

        lastfm_username = LastFmDB().get(member.id)

        if not lastfm_username:
            await interaction.response.send_message(embed=EmbedFunctions().error(f"{member.mention} has not setup their LastFm account.\nTo setup a LastFm account use `/lf set`."), ephemeral=True)
            return

        await interaction.response.defer(with_message = True)

        request_url = requests.get(f"http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&username={lastfm_username}&limit=1&api_key={self.client.lf_network.api_key}&format=json")

        if not request_url.status_code == 200:
            await interaction.followup.send(embed=EmbedFunctions().error("LastFm didn't respond correctly, try in a few minutes again!"))
            return

        np_user_data = request_url.json()
        cover_image = ""
        output = ""

        for track in np_user_data["recenttracks"]["track"]:
            track_url = urllib.parse.quote_plus(track['url'])
            artist_name_for_url = urllib.parse.quote_plus(track['artist']['#text'])
            album_name_for_url = urllib.parse.quote_plus(track['album']['#text'])

            track_name = Get().markdown_safe(track['name'])
            album_name = Get().markdown_safe(track['album']['#text'])
            artist_name = Get().markdown_safe(track['artist']['#text'])

            if "date" in track:
                timestamp = f"<t:{track['date']['uts']}:R>"
                output += f"**[{track_name}]({track_url})** on [{album_name}](https://www.last.fm/music/{artist_name_for_url}/{album_name_for_url}/)\nby [{artist_name}](https://www.last.fm/music/{artist_name_for_url}/) - {timestamp}"
                if cover_image == "":
                    cover_image = track['image'][3]['#text']

            else:
                output += f"`Now Playing:`\n**[{track_name}]({track_url})** on [{album_name}](https://www.last.fm/music/{artist_name_for_url}/{album_name_for_url}/)\nby [{artist_name}](https://www.last.fm/music/{artist_name_for_url}/)\n\n`Previous:\n`"
                cover_image = track['image'][3]['#text']

        embed = EmbedFunctions().builder(
            color = self.client.LASTFM_COLOR,
            thumbnail = cover_image,
            author = f"{member.display_name} is listening to:",
            author_icon = self.client.LASTFM_ICON,
            description = output,
            footer = "DEFAULT_KST_FOOTER"
        )

        await interaction.followup.send(embed=embed)



def setup(client: SomiBot):
    client.add_cog(LastFmNowPlaying(client))