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
from utilities.LastFmButtons import LastFmButtons



async def lastfm_top_artists(interaction, member, lastfm_username, timeframe, page_number, first_message_sent):
    request_url = requests.get(f"http://ws.audioscrobbler.com/2.0/?method=user.gettopartists&username={lastfm_username}&limit=10&page={page_number}&period={timeframe}&api_key={network.api_key}&format=json")

    if not request_url.status_code == 200:
        await interaction.followup.send("LastFm didn't respond correctly, try in a few minutes again!", ephemeral=True)
        return

    top_artists_user_data = request_url.json()
    last_page = int(top_artists_user_data["topartists"]["@attr"]["totalPages"])
    name = get_nick_else_name(member)
    output = ""

    for artist in top_artists_user_data["topartists"]["artist"]:
        output += f"{artist['@attr']['rank']}. **[{artist['name']}]({artist['url']})** - *({artist['playcount']} plays)*\n"

    authot_text_dict = {"7day": "of the past week:", "1month": "of the past month:", "3month": "of the past quarter:", "6month": "of the past half a year:", "12month": "of the past year:", "overall": "of all time:"}
    author_text = f"{name} top artists {authot_text_dict[timeframe]}"

    embed = embed_builder(description = output,
                          color = LASTFM_COLOR,
                          author = author_text,
                          author_icon = LASTFM_ICON,
                          footer = "DEFAULT_KST_FOOTER")

    view = LastFmButtons(page = page_number, last_page = last_page, interaction = interaction)

    if not first_message_sent:
        first_message_sent = True
        await interaction.followup.send(embed=embed, view=view)
    else:
        await interaction.edit_original_message(embed=embed, view=view)

    await view.change_page_button()
    await view.check_page_for_button_deactivation()
    await view.wait()

    if view.value == None:
        uses_update("command_uses", "lf topartists")
        return

    await lastfm_top_artists(interaction, member, lastfm_username, timeframe, page_number = view.page, first_message_sent = first_message_sent)



class LastFmTopArtists(nextcord.ext.commands.Cog):

    def __init__(self, client):
        self.client = client

    from utilities.maincommands import lastfm

    ###lf#top#artists###########################################################

    @lastfm.subcommand(name = "topartists", description = "shows your top artists on LastFm")
    async def top_artists(self,
                         interaction: nextcord.Interaction,
                         *,
                         member: nextcord.Member = nextcord.SlashOption(description="the user you want the top artists of", required=False),
                         timeframe: str = nextcord.SlashOption(description="the timeframe you want the top artists for", required=False, choices = {"Past Week": "7day", "Past Month": "1month", "Past Quarter": "3month", "Past Half a Year": "6month", "Past Year": "12month", "All Time": "overall"})):
        if not checks(interaction.guild, interaction.user):
            return

        if member == None:
            member = interaction.guild.get_member(interaction.user.id)

        if timeframe == None:
            timeframe = "overall"

        print(f"{interaction.user}: /lf topartists {member} {timeframe}")

        lastfm_username = lastfm_get_user_from_db(member.id)

        if not lastfm_username:
            await interaction.response.send_message(f"{member.mention} has not setup their LastFm account.", ephemeral=True)
            return

        await interaction.response.defer(with_message = True)

        await lastfm_top_artists(interaction, member, lastfm_username, timeframe, page_number = 1, first_message_sent = False)



def setup(client):
    client.add_cog(LastFmTopArtists(client))