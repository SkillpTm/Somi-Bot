###package#import###############################################################################

import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
import requests

client = commands.Bot(intents=nextcord.Intents.all())

###self#imports###############################################################################

from cogs._global_data.global_data import network
from database.database_command_uses import uses_update
from database.database_lastfm import lastfm_get_user_from_db, lastfm_set_user, lastfm_reset_user
from utilities.maincommands import checks



class LastFmSet(commands.Cog):

    def __init__(self, client):
        self.client = client

    from utilities.maincommands import lastfm

    ###lf#set###########################################################

    @lastfm.subcommand(name = "set", description = "set your LastFm account")
    async def set(self,
                  interaction: Interaction,
                  *,
                  lastfmname: str = SlashOption(description="input your LastFm name", required=True, min_length=1, max_length=100)):
        if not checks(interaction):
            return

        print(f"{interaction.user}: /lf set {lastfmname}")

        lastfm_username = lastfm_get_user_from_db(interaction.user.id)

        if lastfm_username:
            await interaction.response.send_message(f"You already set a LastFm account. To reset it use `/lf reset`.", ephemeral=True)
            return

        request_url = f"http://ws.audioscrobbler.com/2.0/?method=user.getinfo&username={lastfmname}&api_key={network.api_key}&format=json"

        if not requests.get(request_url).status_code == 200:
            await interaction.response.send_message(f"The user `{lastfmname}` couldn't be found on LastFm.", ephemeral=True)
            return

        recent_user_data = requests.get(request_url).json()
        lastfm_username = recent_user_data["user"]["name"]

        lastfm_set_user(interaction.user.id, lastfm_username)

        await interaction.response.send_message(f"You were succesfully connected with the LastFm user `{lastfm_username}`", ephemeral=True)

        uses_update("command_uses", "lf set")

    ###lf#reset###########################################################

    @lastfm.subcommand(name = "reset", description = "reset your LastFm-Discord account connection")
    async def reset(self,
                    interaction: Interaction):
        if not checks(interaction):
            return

        print(f"{interaction.user}: /lf reset")

        lastfm_username = lastfm_get_user_from_db(interaction.user.id)

        if not lastfm_username:
            await interaction.response.send_message(f"You don't have a LastFm account connected to your discord account.", ephemeral=True)
            return

        lastfm_reset_user(interaction.user.id)

        await interaction.response.send_message(f"You succesfully reset your LastFm-Discord account connection.", ephemeral=True)

        uses_update("command_uses", "lf reset")



def setup(client):
    client.add_cog(LastFmSet(client))