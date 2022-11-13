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



async def lastfm_recent(interaction, member, lastfm_username, page_number, first_message_sent):
    request_url = requests.get(f"http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&username={lastfm_username}&limit=10&page={page_number}&api_key={network.api_key}&format=json")

    if not request_url.status_code == 200:
        await interaction.followup.send("LastFm didn't respond correctly, try in a few minutes again!", ephemeral=True)
        return

    recent_user_data = request_url.json()
    last_page = int(recent_user_data["recenttracks"]["@attr"]["totalPages"])
    name = get_nick_else_name(member)
    output = ""
    i = 0

    for track in recent_user_data["recenttracks"]["track"]:
        i += 1
        artist_name_for_url = track['artist']['#text'].replace(" ", "+")

        if "date" in track:
            timestamp = f"<t:{track['date']['uts']}:R>"
            output += f"{i + (page_number - 1) * 10}. **[{track['name']}]({track['url']})** by [{track['artist']['#text']}](https://www.last.fm/music/{artist_name_for_url}/) - {timestamp}\n"

        else:
            i -= 1
            if page_number == 1:
                timestamp = "*now playing*"
                output += f"{i + (page_number - 1) * 10}. **[{track['name']}]({track['url']})** by [{track['artist']['#text']}](https://www.last.fm/music/{artist_name_for_url}/) - {timestamp}\n"

    embed = embed_builder(description = output,
                          color = LASTFM_COLOR,
                          author = f"{name} recently played:",
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
        uses_update("command_uses", "lf recent")
        return

    await lastfm_recent(interaction, member, lastfm_username, page_number = view.page, first_message_sent = first_message_sent)



class LastFmRecent(nextcord.ext.commands.Cog):

    def __init__(self, client):
        self.client = client

    from utilities.maincommands import lastfm

    ###lf#recent###########################################################

    @lastfm.subcommand(name = "rc", description = "shows your recently played songs on LastFm", name_localizations = {country_tag:"recent" for country_tag in nextcord.Locale})
    async def recent(self,
                     interaction: nextcord.Interaction,
                     *,
                     member: nextcord.Member = nextcord.SlashOption(description="the user you want the recent tracks of", required=False)):
        if not checks(interaction.guild, interaction.user):
            return

        if member == None:
            member = interaction.guild.get_member(interaction.user.id)

        print(f"{interaction.user}: /lf recent {member}")

        lastfm_username = lastfm_get_user_from_db(member.id)

        if not lastfm_username:
            await interaction.response.send_message(f"{member.mention} has not setup their LastFm account.", ephemeral=True)
            return

        await interaction.response.defer(with_message = True)

        await lastfm_recent(interaction, member, lastfm_username, page_number = 1, first_message_sent = False)



def setup(client):
    client.add_cog(LastFmRecent(client))