####################################################################################################

import nextcord
import nextcord.ext.commands as nextcord_C
import nextcord.ext.application_checks as nextcord_AC
import requests

####################################################################################################

from lib.db_modules import LastFmDB
from lib.modules import Checks, EmbedFunctions, Get
from lib.utilities import LASTFM_TIMEFRAMES, LASTFM_TIMEFRAMES_TEXT, PageButtons, SomiBot



class LastFmTopAlbums(nextcord_C.Cog):

    def __init__(self, client):
        self.client: SomiBot = client

    from lib.utilities.main_commands import lastfm

    ####################################################################################################

    @lastfm.subcommand(name = "tal", description = "shows your top albums on LastFm", name_localizations = {country_tag:"topalbums" for country_tag in nextcord.Locale})
    @nextcord_AC.check(Checks().interaction_in_guild())
    async def lastfm_top_albums(self,
                                interaction: nextcord.Interaction,
                                *,
                                member: nextcord.Member = nextcord.SlashOption(description="the user you want the top albums of", required=False),
                                timeframe: str = nextcord.SlashOption(description="the timeframe you want the top albums for", required=False, choices=LASTFM_TIMEFRAMES)):
        """This command shows someone's top albums"""

        if not member:
            member = interaction.guild.get_member(interaction.user.id)

        if not timeframe:
            timeframe = "overall"

        self.client.Loggers.action_log(f"Guild: {interaction.guild.id} ~ Channel: {interaction.channel.id} ~ User: {interaction.user.id} ~ /lf topalbums {member.id} {timeframe}")

        lastfm_username = LastFmDB().get(member.id)

        if not lastfm_username:
            await interaction.response.send_message(embed=EmbedFunctions().error(f"{member.mention} has not setup their LastFm account.\nTo setup a LastFm account use `/lf set`."), ephemeral=True)
            return

        await interaction.response.defer(with_message = True)

        await self.lastfm_top_albums_rec(interaction, member, lastfm_username, timeframe, page_number = 1, first_message_sent = False)

    ####################################################################################################

    async def lastfm_top_albums_rec(self,
                                    interaction: nextcord.Interaction,
                                    member: nextcord.Member,
                                    lastfm_username: str,
                                    timeframe: str,
                                    page_number: int,
                                    first_message_sent: bool) -> None:
        """This function recurses on button press and requests the data from the LastFm api to build the embed"""

        request_url = requests.get(f"http://ws.audioscrobbler.com/2.0/?method=user.gettopalbums&username={lastfm_username}&limit=10&page={page_number}&period={timeframe}&api_key={self.client.lf_network.api_key}&format=json")

        if not request_url.status_code == 200:
            embed = EmbedFunctions().error("LastFm didn't respond correctly, try in a few minutes again!")

            if not first_message_sent:
                await interaction.followup.send(embed=embed)
            else:
                await interaction.edit_original_message(embed=embed, view=None)
                
            return

        top_albums_user_data = request_url.json()
        last_page = int(top_albums_user_data["topalbums"]["@attr"]["totalPages"])
        output = ""

        for album in top_albums_user_data["topalbums"]["album"]:
            album_url = album['url']
            artist_url = album['artist']['url']

            album_name = Get().markdown_safe(album['name'])
            artist_name = Get().markdown_safe(album['artist']['name'])
            output += f"{album['@attr']['rank']}. **[{album_name}]({album_url})** by [{artist_name}]({artist_url}) - *({album['playcount']} plays)*\n"

        embed = EmbedFunctions().builder(
            color = self.client.LASTFM_COLOR,
            author = f"{member.display_name} Top Albums: {LASTFM_TIMEFRAMES_TEXT[timeframe]}",
            author_icon = self.client.LASTFM_ICON,
            description = output,
            footer = "DEFAULT_KST_FOOTER"
        )

        view = PageButtons(page = page_number, last_page = last_page, interaction = interaction)

        if not first_message_sent:
            first_message_sent = True
            await interaction.followup.send(embed=embed, view=view)
        else:
            await interaction.edit_original_message(embed=embed, view=view)

        await view.update_buttons()
        await view.wait()

        if not view.value:
            return

        await self.lastfm_top_albums_rec(interaction, member, lastfm_username, timeframe, view.page, first_message_sent)



def setup(client: SomiBot):
    client.add_cog(LastFmTopAlbums(client))