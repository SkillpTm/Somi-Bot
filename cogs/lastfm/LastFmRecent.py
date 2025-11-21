import urllib.parse

import nextcord
import nextcord.ext.commands as nextcord_C
import requests

from cogs.basic.ParentCommand import ParentCommand
from lib.database import db
from lib.helpers import EmbedFunctions, Get
from lib.managers import Commands, Config, Keychain
from lib.modules import PageButtons, SomiBot



class LastFmRecent(nextcord_C.Cog):

    def __init__(self, client: SomiBot) -> None:
        self.client = client


    @ParentCommand.lastfm.subcommand(
        Commands().data["lf recent"].alias,
        Commands().data["lf recent"].description,
        name_localizations = {country_tag: Commands().data["lf recent"].name for country_tag in nextcord.Locale}
    )
    async def lastfm_recent(
        self,
        interaction: nextcord.Interaction[SomiBot],
        *,
        user: nextcord.User = nextcord.SlashOption(
            Commands().data["lf recent"].parameters["user"].name,
            Commands().data["lf recent"].parameters["user"].description,
            required = False
        )
    ) -> None:
        """This command shows someone's recent tracks and what they are now playing on the first page"""

        user = user or interaction.user

        if not (lastfm_username := str(await db.User.LASTFM.get(interaction.user.id) or "")):
            await interaction.response.send_message(embed=EmbedFunctions().get_error_message(f"{user.mention} has not setup their LastFm account.\nTo setup a LastFm account use `/lf set`."), ephemeral=True)
            return

        await interaction.response.defer(with_message=True)

        await self.lastfm_recent_rec(interaction, user, lastfm_username, page_number = 1)


    async def lastfm_recent_rec(
        self,
        interaction: nextcord.Interaction[SomiBot],
        user: nextcord.User,
        lastfm_username: str,
        page_number: int
    ) -> None:
        """This function recurses on button press and requests the data from the LastFm api to build the embed"""

        np_response = requests.get(f"http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&username={lastfm_username}&limit=10&page={page_number}&api_key={Keychain().LAST_FM_API_KEY}&format=json", timeout=10)

        if np_response.status_code != 200:
            await interaction.edit_original_message(embed=EmbedFunctions().get_error_message("LastFm didn't respond correctly, try in a few minutes again!"), view=None)
            return

        np_data = np_response.json()
        last_page = int(np_data["recenttracks"]["@attr"]["totalPages"])
        output = ""
        index = 0

        # formats the last 10 songs as following in a string:
        # 1. [song name](song link) by [artist](artist link) - timestamp
        for track in np_data["recenttracks"]["track"]:
            index += 1
            track_url = track["url"]
            artist_name_for_url = urllib.parse.quote_plus(track["artist"]["#text"])

            track_name = Get.markdown_safe(track["name"])
            artist_name = Get.markdown_safe(track["artist"]["#text"])
            timestamp = ""

            # set the timestamp, unless it is currently playing
            if "date" in track:
                timestamp = f"<t:{track['date']['uts']}:R>"
            else:
                index -= 1
                if page_number == 1:
                    timestamp = "*now playing*"

            if timestamp != "":
                output += f"{index + (page_number - 1) * 10}. **[{track_name}]({track_url})** by [{artist_name}](https://www.last.fm/music/{artist_name_for_url}/) - {timestamp}\n"

        footer = ""

        if (scrobbles_this_month := int(np_data["recenttracks"]["@attr"]["total"])):
            footer = f"{scrobbles_this_month} scrobbles in the last 30 days"

        embed = EmbedFunctions().builder(
            color = Config().LASTFM_COLOR,
            author = f"{user.display_name} recently played:",
            author_icon = Config().LASTFM_ICON,
            description = output,
            footer = footer,
            footer_icon = Config().HEADPHONES_ICON
        )

        view = PageButtons(page=page_number, last_page=last_page, interaction=interaction) # type: ignore

        await interaction.edit_original_message(embed=embed, view=view)
        await view.update_buttons()
        await view.wait()

        if not view.value:
            return

        await self.lastfm_recent_rec(interaction, user, lastfm_username, view.page)



def setup(client: SomiBot) -> None:
    client.add_cog(LastFmRecent(client))