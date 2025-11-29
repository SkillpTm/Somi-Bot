import nextcord
import nextcord.ext.commands as nextcord_C

from cogs.events.PurgeLog import PurgeLog
from lib.helpers import EmbedFunctions
from lib.managers import Commands
from lib.modules import SomiBot



class Purge(nextcord_C.Cog):

    def __init__(self, client: SomiBot) -> None:
        self.client = client


    @nextcord.slash_command(
        Commands().data["purge"].alias,
        Commands().data["purge"].description,
        name_localizations = {country_tag: Commands().data["purge"].name for country_tag in nextcord.Locale},
        default_member_permissions = nextcord.Permissions(manage_messages=True),
        integration_types = [nextcord.IntegrationType.guild_install],
        contexts = [nextcord.InteractionContextType.guild]
    )
    async def purge(
        self,
        interaction: nextcord.Interaction[SomiBot],
        *,
        amount: int = nextcord.SlashOption(
            Commands().data["purge"].parameters["amount"].name,
            Commands().data["purge"].parameters["amount"].description,
            required = True,
            min_value = 1,
            max_value = 1000
        )
    ) -> None:
        """This command removes the given amount of last messages from a channel."""

        await interaction.response.defer(ephemeral=True, with_message=True)
        messages = await interaction.channel.purge(limit=amount) # type: ignore
        await interaction.send(embed=EmbedFunctions.get_success_message(f"Succesfully purged the last `{amount}` messages from {interaction.channel.mention}.")) # type: ignore
        await PurgeLog.send_purge_log(messages, interaction.user) # type: ignore



def setup(client: SomiBot) -> None:
    client.add_cog(Purge(client))