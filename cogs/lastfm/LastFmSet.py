import nextcord
import nextcord.ext.commands as nextcord_C
import nextcord.ext.application_checks as nextcord_AC
import requests

from lib.db_modules import LastFmDB
from lib.modules import Checks, EmbedFunctions, Get
from lib.utilities import SomiBot



class LastFmSet(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    from lib.utilities.main_commands import lastfm

    ####################################################################################################

    @lastfm.subcommand(name = "set", description = "set your LastFm account")
    @nextcord_AC.check(Checks().interaction_not_by_bot())
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

        self.client.Loggers.action_log(Get().log_message(
            interaction,
            "/lf set",
            {"lastfmname": lastfmname}
        ))

        await interaction.response.defer(ephemeral=True, with_message = True)

        lastfm_username = LastFmDB().get(interaction.user.id)

        if lastfm_username:
            await interaction.followup.send(embed=EmbedFunctions().error(f"You already set a LastFm account.\nTo reset your LastFm account use `/lf reset`."), ephemeral=True)
            return

        info_response = requests.get(f"http://ws.audioscrobbler.com/2.0/?method=user.getinfo&username={lastfmname}&api_key={self.client.Keychain.LAST_FM_API_KEY}&format=json")

        if info_response.status_code != 200:
            await interaction.followup.send(embed=EmbedFunctions().error(f"The user `{lastfmname}` couldn't be found on LastFm."), ephemeral=True)
            return

        username_response = info_response["user"]["name"]

        LastFmDB().add(interaction.user.id, username_response)

        await interaction.followup.send(embed=EmbedFunctions().success(f"You were succesfully connected with the LastFm user `{username_response}`"), ephemeral=True)

    ####################################################################################################

    @lastfm.subcommand(name = "reset", description = "reset your LastFm-Discord account connection")
    @nextcord_AC.check(Checks().interaction_not_by_bot())
    async def lastfm_reset(self, interaction: nextcord.Interaction) -> None:
        """This command deletes the user's connection from the db"""

        self.client.Loggers.action_log(Get().log_message(interaction, "/lf reset"))

        lastfm_username = LastFmDB().get(interaction.user.id)

        if not lastfm_username:
            await interaction.response.send_message(embed=EmbedFunctions().error("You don't have a LastFm account setup."), ephemeral=True)
            return

        LastFmDB().delete(interaction.user.id)

        await interaction.response.send_message(embed=EmbedFunctions().success("You succesfully reset your LastFm account."), ephemeral=True)



def setup(client: SomiBot) -> None:
    client.add_cog(LastFmSet(client))