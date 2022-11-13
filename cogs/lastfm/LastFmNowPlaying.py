###package#import###############################################################################

import nextcord
import requests

client = nextcord.ext.commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from cogs._global_data.GlobalData import network
from database.database_command_uses import uses_update
from database.database_lastfm import lastfm_get_user_from_db
from utilities.maincommands import checks
from utilities.variables import LASTFM_ICON, LASTFM_COLOR
from utilities.partial_commands import get_nick_else_name, embed_builder



class LastFmNowPlaying(nextcord.ext.commands.Cog):

    def __init__(self, client):
        self.client = client

    from utilities.maincommands import lastfm

    ###lf#np###########################################################

    @lastfm.subcommand(name = "np", description = "shows what someone is listening to right now")
    async def now_playing(self,
                 interaction: nextcord.Interaction,
                 *,
                 member: nextcord.Member = nextcord.SlashOption(description="the user you want to be shown, what they're listening to", required=False)):
        if not checks(interaction.guild, interaction.user):
            return

        if member == None:
            member = interaction.guild.get_member(interaction.user.id)

        print(f"{interaction.user}: /lf np {member}")

        lastfm_username = lastfm_get_user_from_db(member.id)

        await interaction.response.defer(with_message = True)

        if not lastfm_username:
            await interaction.followup.send(f"{member.mention} has not setup their LastFm account.", ephemeral=True)
            return

        request_url = requests.get(f"http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&username={lastfm_username}&limit=1&api_key={network.api_key}&format=json")

        if not request_url.status_code == 200:
            await interaction.followup.send("LastFm didn't respond correctly, try in a few minutes again!", ephemeral=True)
            return

        np_user_data = request_url.json()
        name = get_nick_else_name(member)
        cover_image = ""
        output = ""

        for track in np_user_data["recenttracks"]["track"]:
            artist_name_for_url = track['artist']['#text'].replace(" ", "+")
            album_name_for_url = track['album']['#text'].replace(" ", "+")

            if "date" in track:
                timestamp = f"<t:{track['date']['uts']}:R>"
                output += f"**[{track['name']}]({track['url']})** on [{track['album']['#text']}](https://www.last.fm/music/{artist_name_for_url}/{album_name_for_url}/)\nby [{track['artist']['#text']}](https://www.last.fm/music/{artist_name_for_url}/) - {timestamp}"
                if cover_image == "":
                    cover_image = track['image'][3]['#text']

            else:
                output += f"`Now Playing:`\n**[{track['name']}]({track['url']})** on [{track['album']['#text']}](https://www.last.fm/music/{artist_name_for_url}/{album_name_for_url}/)\nby [{track['artist']['#text']}](https://www.last.fm/music/{artist_name_for_url}/)\n\n`Previous:\n`"
                cover_image = track['image'][3]['#text']

        embed = embed_builder(description = output,
                              color = LASTFM_COLOR,
                              thumbnail = cover_image,
                              author = f"{name} is listening to:",
                              author_icon = LASTFM_ICON,
                              footer = "DEFAULT_KST_FOOTER")

        await interaction.followup.send(embed=embed)

        uses_update("command_uses", "lf np")



def setup(client):
    client.add_cog(LastFmNowPlaying(client))