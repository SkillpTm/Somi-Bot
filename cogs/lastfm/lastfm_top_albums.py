###package#import###############################################################################

import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
import requests

client = commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from cogs._global_data.global_data import network
from database.database_command_uses import uses_update
from database.database_lastfm import lastfm_get_user_from_db
from utilities.maincommands import checks
from utilities.variables import LASTFM_ICON, LASTFM_COLOR
from utilities.partial_commands import get_nick_else_name, embed_builder



class LastFmTopAlbumsButtons(nextcord.ui.View):
    def __init__(self, page, last_page):
        self.value = None
        self.page: int = page
        self.last_page: int = last_page
        super().__init__(timeout = 60)

    @nextcord.ui.button(label = "start", style=nextcord.ButtonStyle.green)
    async def lf_top_albums_start(self,
                                  button: nextcord.ui.Button,
                                  interaction: Interaction):
        self.page = 1
        self.value = True
        self.stop()

    @nextcord.ui.button(label = "<<", style=nextcord.ButtonStyle.green)
    async def lf_top_albums_left(self,
                                 button: nextcord.ui.Button,
                                 interaction: Interaction):
        self.page -= 1
        if self.page == 0:
            self.page = 1
        self.value = True
        self.stop()

    @nextcord.ui.button(label = ">>", style=nextcord.ButtonStyle.red)
    async def lf_top_albums_right(self,
                                  button: nextcord.ui.Button,
                                  interaction: Interaction):
        self.page += 1
        if self.page > self.last_page:
            self.page = self.last_page
        self.value = True
        self.stop()

    @nextcord.ui.button(label = "end", style=nextcord.ButtonStyle.red)
    async def lf_top_albums_end(self,
                                button: nextcord.ui.Button,
                                interaction: Interaction):
        self.page = self.last_page
        self.value = True
        self.stop()

    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        await message.edit(view=self)



async def lastfm_top_albums(interaction, member, timeframe, page_number, first_message_sent):
    lastfm_username = lastfm_get_user_from_db(member.id)

    if not lastfm_username:
        await interaction.response.send_message(f"{member.mention} has not setup their LastFm account.", ephemeral=True)
        return

    request_url = f"http://ws.audioscrobbler.com/2.0/?method=user.gettopalbums&username={lastfm_username}&limit=10&page={page_number}&period={timeframe}&api_key={network.api_key}&format=json"

    if not requests.get(request_url).status_code == 200:
        await interaction.response.send_message(f"The user `{lastfm_username}` couldn't be found on LastFm.", ephemeral=True)
        return

    top_albums_user_data = requests.get(request_url).json()
    lastpage = int(top_albums_user_data["topalbums"]["@attr"]["totalPages"])
    name = get_nick_else_name(member)
    output = ""

    for album in top_albums_user_data["topalbums"]["album"]:
        output += f"{album['@attr']['rank']}. **[{album['name']}]({album['url']})** by [{album['artist']['name']}]({album['artist']['url']}) - *({album['playcount']} plays)*\n"

    authot_text_dict = {"7day": "of the past week:", "1month": "of the past month:", "3month": "of the past quarter:", "6month": "of the past half a year:", "12month": "of the past year", "overall": "of all time"}
    author_text = f"{name} top albums {authot_text_dict[timeframe]}"

    embed = embed_builder(description = output,
                          color = LASTFM_COLOR,
                          author = author_text,
                          author_icon = LASTFM_ICON,
                          footer = f"Page {page_number} of {lastpage}")

    view = LastFmTopAlbumsButtons(page = page_number, last_page = lastpage)

    global message

    if not first_message_sent:
        message = await interaction.send(embed=embed, view=view)
    else:
        await first_message_sent.edit(embed=embed, view=view)
        message = first_message_sent

    await view.wait()

    if view.value == None:
        uses_update("command_uses", "lf topalbums")
        return

    await lastfm_top_albums(interaction, member, timeframe, page_number = view.page, first_message_sent = message)



class LastFmTopAlbums(commands.Cog):

    def __init__(self, client):
        self.client = client

    from utilities.maincommands import lastfm

    ###lf#top#albums###########################################################

    @lastfm.subcommand(name = "topalbums", description = "shows your top albums on LastFm")
    async def top_albums(self,
                         interaction: Interaction,
                         *,
                         member: nextcord.Member = SlashOption(description="the user you want the top albums of", required=False),
                         timeframe: str = SlashOption(description="the timeframe you want the top albums for", required=False, choices = {"Past Week": "7day", "Past Month": "1month", "Past Quarter": "3month", "Past Half a Year": "6month", "Past Year": "12month", "All Time": "overall"})):
        if not checks(interaction):
            return

        if member == None:
            member = interaction.guild.get_member(interaction.user.id)

        if timeframe == None:
            timeframe = "overall"

        print(f"{interaction.user}: /lf topalbums {member} {timeframe}")

        await lastfm_top_albums(interaction, member, timeframe, page_number = 1, first_message_sent = False)



def setup(client):
    client.add_cog(LastFmTopAlbums(client))