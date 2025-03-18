import nextcord
import nextcord.ext.commands as nextcord_C
import requests
import urllib.parse

from lib.modules import EmbedFunctions, Get
from lib.utilities import SomiBot



class Lyrics(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    @nextcord.slash_command(
        name = 'genius',
        description = 'Posts the link to the lyircs of the song you are playing',
        name_localizations = {country_tag:"lyrics" for country_tag in nextcord.Locale}
    )
    async def lyrics(
        self,
        interaction: nextcord.Interaction,
        *,
        artist: str = nextcord.SlashOption(
            description = "the artist you want a song to get the lyrics of",
            required = False,
            min_length = 2,
            max_length = 100
        ),
        song: str = nextcord.SlashOption(
            description = "the song of that artist you want to get the lyrics of",
            required = False,
            min_length = 2,
            max_length = 100
        )
    ) -> None:
        """This command will post a link to the lyrics of a song, through the slash options or by pulling it from their Spotify connection with Discord"""

        # if the user didn't provide an artist and song pull what they're listening to from Spotify
        if not artist and not song:
            if not interaction.guild:
                await interaction.response.send_message(embed=EmbedFunctions().get_error_message("Please select a valid artist **and** a valid song!"), ephemeral=True)
                return

            for activity in interaction.guild.get_member(interaction.user.id).activities:
                if isinstance(activity, nextcord.Spotify):
                    artist = activity.artist
                    song = activity.title
                    break

        self.client.Loggers.action_log(Get.log_message(
            interaction,
            "/lyrics",
            {"artist": artist, "song": song}
        ))

        if not artist or not song:
            await interaction.response.send_message(embed=EmbedFunctions().get_error_message("Please select a valid artist **and** a valid song or play a song on Spotify!"), ephemeral=True)
            return

        # search genius for a matching song
        search_response = requests.get(
            f"https://api.genius.com/search?q={urllib.parse.quote_plus(f'{artist}+{song}')}",
            headers={"Authorization": f"Bearer {self.client.Keychain.GENIUS_ACCESS_TOKEN}"}
        ).json()

        # make sure there are results and they're songs
        if not search_response["response"]["hits"] or search_response["response"]["hits"][0]["type"] != "song":
            await interaction.response.send_message(embed=EmbedFunctions().get_error_message("Please select a valid artist **and** a valid song or play a song on Spotify!"), ephemeral=True)
            return
        
        await interaction.response.defer(with_message=True)
        
        # use the first result's ID to find the lyrics page
        song_response = requests.get(
            f"https://api.genius.com/songs/{search_response["response"]["hits"][0]["result"]["id"]}",
            headers={"Authorization": f"Bearer {self.client.Keychain.GENIUS_ACCESS_TOKEN}"}
        )

        if song_response.status_code != 200:
            await interaction.followup.send(embed=EmbedFunctions().get_error_message(f"Genius couldn't find: `{artist}` - `{song}`, please try again!"))
            return
        
        song_data = song_response.json()


        embed = EmbedFunctions().builder(
            color = self.client.GENIUS_COLOR,
            image = song_data["response"]["song"]["song_art_image_url"],
            title = f"Click Here: {song_data['response']['song']['title']}",
            title_url = song_data["response"]["song"]["url"],
            footer = "Lyrics powered by Genius",
            footer_icon = self.client.GENIUS_ICON
        )

        await interaction.followup.send(embed=embed)



def setup(client: SomiBot) -> None:
    client.add_cog(Lyrics(client))