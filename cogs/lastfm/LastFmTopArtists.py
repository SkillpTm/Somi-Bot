####################################################################################################

import nextcord
import nextcord.ext.commands as nextcord_C
import nextcord.ext.application_checks as nextcord_AC
import requests

####################################################################################################

from lib.db_modules import LastFmDB
from lib.modules import Checks, EmbedFunctions, Get
from lib.utilities import LASTFM_TIMEFRAMES, LASTFM_TIMEFRAMES_TEXT, PageButtons, SomiBot



class LastFmTopArtists(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    from lib.utilities.main_commands import lastfm

    ####################################################################################################

    @lastfm.subcommand(name = "tar", description = "shows your top artists on LastFm", name_localizations = {country_tag:"topartists" for country_tag in nextcord.Locale})
    @nextcord_AC.check(Checks().interaction_not_by_bot())
    async def lastfm_top_artists(
        self,
        interaction: nextcord.Interaction,
        *,
        user: nextcord.User = nextcord.SlashOption(
            description="the user you want the top artists of",
            required=False
        ),
        timeframe: str = nextcord.SlashOption(
            description="the timeframe you want the top artists for",
            required=False,
            choices=LASTFM_TIMEFRAMES
        )
    ) -> None:
        """This command shows someone's top artists"""

        if not user:
            user = interaction.user

        if not timeframe:
            timeframe = "overall"

        self.client.Loggers.action_log(Get().log_message(
            interaction,
            "/lf topartists",
            {"user": str(user.id), "timeframe": timeframe}
        ))

        lastfm_username = LastFmDB().get(user.id)

        if not lastfm_username:
            await interaction.response.send_message(embed=EmbedFunctions().error(f"{user.mention} has not setup their LastFm account.\nTo setup a LastFm account use `/lf set`."), ephemeral=True)
            return

        # send a dummy respone to be updated in the recursive function
        await interaction.response.send_message(embed=EmbedFunctions().builder(title=" "))

        await self.lastfm_top_artists_rec(interaction, user, lastfm_username, timeframe, page_number = 1)

        ####################################################################################################

    async def lastfm_top_artists_rec(
        self,
        interaction: nextcord.Interaction,
        member: nextcord.Member,
        lastfm_username: str,
        timeframe: str,
        page_number: int
    ) -> None:
        """This function recurses on button press and requests the data from the LastFm api to build the embed"""

        top_artists_response = requests.get(f"http://ws.audioscrobbler.com/2.0/?method=user.gettopartists&username={lastfm_username}&limit=10&page={page_number}&period={timeframe}&api_key={self.client.lf_network.api_key}&format=json")

        if top_artists_response.status_code != 200:
            await interaction.edit_original_message(embed=EmbedFunctions().error("LastFm didn't respond correctly, try in a few minutes again!"), view=None)
            return

        top_artists_data = top_artists_response.json()
        last_page = int(top_artists_data["topartists"]["@attr"]["totalPages"])
        output = ""

        for artist in top_artists_data["topartists"]["artist"]:
            artist_url = artist['url']
            
            artist_name = Get().markdown_safe(artist['name'])
            output += f"{artist['@attr']['rank']}. **[{artist_name}]({artist_url})** - *({artist['playcount']} plays)*\n"

        embed = EmbedFunctions().builder(
            color = self.client.LASTFM_COLOR,
            author = f"{member.display_name} Top Artists: {LASTFM_TIMEFRAMES_TEXT[timeframe]}",
            author_icon = self.client.LASTFM_ICON,
            description = output,
            footer = "DEFAULT_KST_FOOTER"
        )

        view = PageButtons(page = page_number, last_page = last_page, interaction = interaction)

        await interaction.edit_original_message(embed=embed, view=view)
        await view.update_buttons()
        await view.wait()

        if not view.value:
            return

        await self.lastfm_top_artists_rec(interaction, member, lastfm_username, timeframe, view.page)



def setup(client: SomiBot) -> None:
    client.add_cog(LastFmTopArtists(client))