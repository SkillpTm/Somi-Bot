import nextcord
import nextcord.ext.commands as nextcord_C
import requests

from lib.dbModules import DBHandler
from lib.modules import EmbedFunctions, Get
from lib.utilities import SomiBot



class LastFmSet(nextcord_C.Cog):

    from cogs.basic.ParentCommand import ParentCommand

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    @ParentCommand.lastfm.subcommand(name="set", description="set your LastFm account")
    async def lastfm_set(
        self,
        interaction: nextcord.Interaction,
        *,
        lastfmname: str = nextcord.SlashOption(
            description = "input your LastFm name",
            required = True,
            min_length = 2,
            max_length = 100
        )
    ) -> None:
        """This command connects a discord user and a lastfm account in the db"""

        self.client.Loggers.action_log(Get.log_message(
            interaction,
            "/lf set",
            {"lastfmname": lastfmname}
        ))

        await interaction.response.defer(ephemeral=True, with_message = True)

        info_response = requests.get(f"http://ws.audioscrobbler.com/2.0/?method=user.getinfo&username={lastfmname}&api_key={self.client.Keychain.LAST_FM_API_KEY}&format=json")

        if info_response.status_code != 200:
            await interaction.followup.send(embed=EmbedFunctions().get_error_message(f"The user `{lastfmname}` couldn't be found on LastFm."), ephemeral=True)
            return

        username_response = info_response.json()["user"]["name"]

        await (await DBHandler(self.client.PostgresDB, user_id=interaction.user.id).user()).last_fm_set(username_response)

        await interaction.followup.send(embed=EmbedFunctions().get_success_message(f"You were succesfully connected with the LastFm user `{username_response}`"), ephemeral=True)

    ####################################################################################################

    @ParentCommand.lastfm.subcommand(name="reset", description="reset your LastFm-Discord account connection")
    async def lastfm_reset(self, interaction: nextcord.Interaction) -> None:
        """This command deletes the user's connection from the db"""

        self.client.Loggers.action_log(Get.log_message(interaction, "/lf reset"))

        if not await (await DBHandler(self.client.PostgresDB, user_id=interaction.user.id).user()).last_fm_reset():
            await interaction.response.send_message(embed=EmbedFunctions().get_error_message("You don't have a LastFm account setup."), ephemeral=True)
            return

        await interaction.response.send_message(embed=EmbedFunctions().get_success_message("You succesfully reset your LastFm account."), ephemeral=True)



def setup(client: SomiBot) -> None:
    client.add_cog(LastFmSet(client))