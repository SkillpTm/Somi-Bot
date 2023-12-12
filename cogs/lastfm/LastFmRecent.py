####################################################################################################

import nextcord
import nextcord.ext.commands as nextcord_C
import nextcord.ext.application_checks as nextcord_AC
import requests
import urllib.parse

####################################################################################################

from lib.db_modules import LastFmDB
from lib.modules import Checks, EmbedFunctions, Get
from lib.utilities import PageButtons, SomiBot



class LastFmRecent(nextcord_C.Cog):

    def __init__(self, client):
        self.client: SomiBot = client

    from lib.utilities.main_commands import lastfm

    ####################################################################################################

    @lastfm.subcommand(name = "rc", description = "shows your recently played songs on LastFm", name_localizations = {country_tag:"recent" for country_tag in nextcord.Locale})
    @nextcord_AC.check(Checks().interaction_in_guild())
    async def lastfm_recent(self,
                            interaction: nextcord.Interaction,
                            *,
                            member: nextcord.Member = nextcord.SlashOption(description="the user you want the recent tracks of", required=False)):
        """This command shows someone's recent tracks and what they are now playing on the first page"""

        if not member:
            member = interaction.guild.get_member(interaction.user.id)

        self.client.Loggers.action_log(f"Guild: {interaction.guild.id} ~ Channel: {interaction.channel.id} ~ User: {interaction.user.id} ~ /lf recent {member.id}")

        lastfm_username = LastFmDB().get_user(member.id)

        if not lastfm_username:
            await interaction.response.send_message(embed=EmbedFunctions().error(f"{member.mention} has not setup their LastFm account.\nTo setup a LastFm account use `/lf set`."), ephemeral=True)
            return

        await interaction.response.defer(with_message = True)

        await self.lastfm_recent_rec(interaction, member, lastfm_username, page_number = 1, first_message_sent = False)

    ####################################################################################################

    async def lastfm_recent_rec(self,
                                interaction: nextcord.Interaction,
                                member: nextcord.Member,
                                lastfm_username: str,
                                page_number: int,
                                first_message_sent: bool) -> None:
        """This function recurses on button press and requests the data from the LastFm api to build the embed"""

        request_url = requests.get(f"http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&username={lastfm_username}&limit=10&page={page_number}&api_key={self.client.lf_network.api_key}&format=json")

        if not request_url.status_code == 200:
            embed = EmbedFunctions().error("LastFm didn't respond correctly, try in a few minutes again!")

            if not first_message_sent:
                await interaction.followup.send(embed=embed)
            else:
                await interaction.edit_original_message(embed=embed, view=None)
                
            return

        recent_user_data = request_url.json()
        last_page = int(recent_user_data["recenttracks"]["@attr"]["totalPages"])
        output = ""
        i = 0

        for track in recent_user_data["recenttracks"]["track"]:
            i += 1
            track_url = Get().markdown_safe(track['url'])
            artist_name_for_url = urllib.parse.quote_plus(track['artist']['#text'])

            track_name = Get().markdown_safe(track['name'])
            artist_name = Get().markdown_safe(track['artist']['#text'])
            timestamp = ""

            if "date" in track:
                timestamp = f"<t:{track['date']['uts']}:R>"
            else:
                i -= 1
                if page_number == 1:
                    timestamp = "*now playing*"

            if timestamp != "":
                output += f"{i + (page_number - 1) * 10}. **[{track_name}]({track_url})** by [{artist_name}](https://www.last.fm/music/{artist_name_for_url}/) - {timestamp}\n"

        embed = EmbedFunctions().builder(
            color = self.client.LASTFM_COLOR,
            author = f"{member.display_name} recently played:",
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

        await self.lastfm_recent_rec(interaction, member, lastfm_username, view.page, first_message_sent)



def setup(client: SomiBot):
    client.add_cog(LastFmRecent(client))