import nextcord
import nextcord.ext.commands as nextcord_C
import requests

from lib.database import db
from lib.helpers import EmbedFunctions
from lib.managers import Commands, Keychain
from lib.modules import SomiBot



class LastFmSet(nextcord_C.Cog):

    from cogs.basic.ParentCommand import ParentCommand

    def __init__(self, client) -> None:
        self.client: SomiBot = client


    @ParentCommand.lastfm.subcommand(Commands().data["lf set"].name, Commands().data["lf set"].description)
    async def lastfm_set(
        self,
        interaction: nextcord.Interaction,
        *,
        lastfm_username: str = nextcord.SlashOption(
            Commands().data["lf set"].parameters["lastfm_username"].name,
            Commands().data["lf set"].parameters["lastfm_username"].description,
            required = True,
            min_length = 2,
            max_length = 100
        )
    ) -> None:
        """This command connects a discord user and a lastfm account in the db"""

        await interaction.response.defer(ephemeral=True, with_message=True)

        info_response = requests.get(f"http://ws.audioscrobbler.com/2.0/?method=user.getinfo&username={lastfm_username}&api_key={Keychain().LAST_FM_API_KEY}&format=json", timeout=10)

        if info_response.status_code != 200:
            await interaction.followup.send(embed=EmbedFunctions().get_error_message(f"The user `{lastfm_username}` couldn't be found on LastFm."), ephemeral=True)
            return

        username_response = info_response.json()["user"]["name"]

        await db.User.LASTFM.set(interaction.user.id, username_response)

        await interaction.followup.send(embed=EmbedFunctions().get_success_message(f"You were succesfully connected with the LastFm user `{username_response}`"), ephemeral=True)


    @ParentCommand.lastfm.subcommand(Commands().data["lf reset"].name, Commands().data["lf reset"].description)
    async def lastfm_reset(self, interaction: nextcord.Interaction) -> None:
        """This command deletes the user's connection from the db"""

        if not await db.User.LASTFM.get(interaction.user.id):
            await interaction.response.send_message(embed=EmbedFunctions().get_error_message("You don't have a LastFm account setup."), ephemeral=True)
            return
        
        await db.User.LASTFM.set(interaction.user.id, None)

        await interaction.response.send_message(embed=EmbedFunctions().get_success_message("You succesfully reset your LastFm account."), ephemeral=True)



def setup(client: SomiBot) -> None:
    client.add_cog(LastFmSet(client))