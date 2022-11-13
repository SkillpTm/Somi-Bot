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



class LastFmRecentButtons(nextcord.ui.View):
    def __init__(self, page, last_page):
        self.value = None
        self.page: int = page
        self.last_page: int = last_page
        super().__init__(timeout = 60)

    @nextcord.ui.button(label = "start", style=nextcord.ButtonStyle.green)
    async def lf_recent_start(self,
                              button: nextcord.ui.Button,
                              interaction: Interaction):
        self.page = 1
        self.value = True
        self.stop()

    @nextcord.ui.button(label = "<<", style=nextcord.ButtonStyle.green)
    async def lf_recent_left(self,
                             button: nextcord.ui.Button,
                             interaction: Interaction):
        self.page -= 1
        if self.page == 0:
            self.page = 1
        self.value = True
        self.stop()

    @nextcord.ui.button(label = ">>", style=nextcord.ButtonStyle.red)
    async def lf_recent_right(self,
                              button: nextcord.ui.Button,
                              interaction: Interaction):
        self.page += 1
        if self.page > self.last_page:
            self.page = self.last_page
        self.value = True
        self.stop()

    @nextcord.ui.button(label = "end", style=nextcord.ButtonStyle.red)
    async def lf_recent_end(self,
                            button: nextcord.ui.Button,
                            interaction: Interaction):
        self.page = self.last_page
        self.value = True
        self.stop()

    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        await message.edit(view=self)



async def lastfm_recent(interaction, member, page_number, first_message_sent):
    lastfm_username = lastfm_get_user_from_db(member.id)

    if not lastfm_username:
        await interaction.response.send_message(f"{member.mention} has not setup their LastFm account.", ephemeral=True)
        return

    request_url = f"http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&username={lastfm_username}&limit=10&page={page_number}&api_key={network.api_key}&format=json"

    if not requests.get(request_url).status_code == 200:
        await interaction.response.send_message(f"The user `{lastfm_username}` couldn't be found on LastFm.", ephemeral=True)
        return

    recent_user_data = requests.get(request_url).json()
    lastpage = int(recent_user_data["recenttracks"]["@attr"]["totalPages"])
    name = get_nick_else_name(member)
    output = ""
    i = 0

    for track in recent_user_data["recenttracks"]["track"]:
        i += 1
        artist_name_for_url = track['artist']['#text'].replace(" ", "+")

        try:
            timestamp = f"<t:{track['date']['uts']}:R>"
            output += f"{i + (page_number - 1) * 10}. **[{track['name']}]({track['url']})** by [{track['artist']['#text']}](https://www.last.fm/music/{artist_name_for_url}/) - {timestamp}\n"

        except:
            i -= 1
            if page_number == 1:
                timestamp = "*now playing*"
                output += f"{i + (page_number - 1) * 10}. **[{track['name']}]({track['url']})** by [{track['artist']['#text']}](https://www.last.fm/music/{artist_name_for_url}/) - {timestamp}\n"

    embed = embed_builder(description = output,
                          color = LASTFM_COLOR,
                          author = f"{name} recently played:",
                          author_icon = LASTFM_ICON,
                          footer = f"Page {page_number} of {lastpage}")

    view = LastFmRecentButtons(page = page_number, last_page = lastpage)

    global message

    if not first_message_sent:
        message = await interaction.send(embed=embed, view=view)
    else:
        await first_message_sent.edit(embed=embed, view=view)
        message = first_message_sent

    await view.wait()

    if view.value == None:
        uses_update("command_uses", "lf recent")
        return

    await lastfm_recent(interaction, member, page_number = view.page, first_message_sent = message)



class LastFmRecent(commands.Cog):

    def __init__(self, client):
        self.client = client

    from utilities.maincommands import lastfm

    ###lf#recent###########################################################

    @lastfm.subcommand(name = "recent", description = "shows your recently played songs on LastFm")
    async def recent(self,
                     interaction: Interaction,
                     *,
                     member: nextcord.Member = SlashOption(description="the user you want the recent tracks of", required=False)):
        if not checks(interaction):
            return

        if member == None:
            member = interaction.guild.get_member(interaction.user.id)

        print(f"{interaction.user}: /lf recent {member}")

        await lastfm_recent(interaction, member, page_number = 1, first_message_sent = False)



def setup(client):
    client.add_cog(LastFmRecent(client))