import time

import nextcord
import nextcord.ext.commands as nextcord_C
import requests

from lib.database import db
from lib.helpers import EmbedField, EmbedFunctions, Get
from lib.managers import Commands, Config, Keychain
from lib.modules import SomiBot



class LastFmProfile(nextcord_C.Cog):

    from cogs.basic.ParentCommand import ParentCommand

    def __init__(self, client: SomiBot) -> None:
        self.client = client


    @ParentCommand.lastfm.subcommand(Commands().data["lf profile"].name, Commands().data["lf profile"].description)
    async def lastfm_profile(
        self,
        interaction: nextcord.Interaction[SomiBot],
        *,
        user: nextcord.User = nextcord.SlashOption(
            Commands().data["lf profile"].parameters["user"].name,
            Commands().data["lf profile"].parameters["user"].description,
            required = False
        )
    ) -> None:
        """This command outputs information about a user's lastfm account"""

        user = user or interaction.user

        if not (lastfm_username := str(await db.User.LASTFM.get(interaction.user.id) or "")):
            await interaction.response.send_message(embed=EmbedFunctions().get_error_message(f"{user.mention} has not setup their LastFm account.\nTo setup a LastFm account use `/lf set`."), ephemeral=True)
            return

        await interaction.response.defer(with_message=True)

        profile_response = requests.get(f"http://ws.audioscrobbler.com/2.0/?method=user.getinfo&username={lastfm_username}&limit=1&api_key={Keychain().LAST_FM_API_KEY}&format=json", timeout=10)

        if profile_response.status_code != 200:
            await interaction.followup.send(embed=EmbedFunctions().get_error_message("LastFm didn't respond correctly, try in a few minutes again!"))
            return

        profile_user_data = profile_response.json()

        # set a default pfp if the user doesn't have one
        if profile_user_data["user"]["image"][3]["#text"]:
            lastfm_user_pfp = profile_user_data["user"]["image"][3]["#text"]
        else:
            lastfm_user_pfp = Config().DEFAULT_PFP

        days_plays_ratio = round(int(profile_user_data["user"]["playcount"]) / (int((int(time.time()) - int(profile_user_data["user"]["registered"]["unixtime"])) / 60 / 60 / 24)), 2)

        footer = ""

        if (scrobbles_this_month := Get.lf_scrobbles_this_month(lastfm_username)) is not None:
            footer = f"{scrobbles_this_month} scrobbles in the last 30 days"

        embed = EmbedFunctions().builder(
            color = Config().LASTFM_COLOR,
            thumbnail = lastfm_user_pfp,
            author = f"{user.display_name} LastFm User Data",
            author_icon = Config().LASTFM_ICON,
            footer = footer,
            footer_icon = Config().HEADPHONES_ICON,
            fields = [
                EmbedField(
                    "LastFm name:",
                    f"[{Get.markdown_safe(profile_user_data['user']['name'])}]({profile_user_data['user']['url']})",
                    True
                ),
                EmbedField(
                    "Total Plays:",
                    f"__**{profile_user_data['user']['playcount']}**__",
                    True
                ),
                EmbedField(
                    "Average Plays/Day:",
                    f"{days_plays_ratio}",
                    True
                ),
                EmbedField(
                    "Registered at:",
                    f"<t:{int(profile_user_data['user']['registered']['unixtime'])}>",
                    False
                ),
                EmbedField(
                    "Unique Artists:",
                    profile_user_data["user"]["artist_count"],
                    True
                ),
                EmbedField(
                    "Unique Albums:",
                    profile_user_data["user"]["album_count"],
                    True
                ),
                EmbedField(
                    "Unique Tracks:",
                    profile_user_data["user"]["track_count"],
                    True
                )
            ]
        )

        await interaction.followup.send(embed=embed)



def setup(client: SomiBot) -> None:
    client.add_cog(LastFmProfile(client))