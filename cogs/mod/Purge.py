import nextcord
import nextcord.ext.commands as nextcord_C
import nextcord.ext.application_checks as nextcord_AC

from lib.modules import Checks, EmbedFunctions, Get
from lib.utilities import SomiBot



class Purge(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    @nextcord.slash_command(
        name = "clear",
        description = "clears the entered amount of messages in a channel",
        default_member_permissions = nextcord.Permissions(manage_messages=True),
        name_localizations = {country_tag:"purge" for country_tag in nextcord.Locale},
        integration_types = [nextcord.IntegrationType.guild_install],
        contexts = [nextcord.InteractionContextType.guild]
    )
    @nextcord_AC.check(Checks.interaction_not_by_bot() and Checks.interaction_in_guild)
    async def purge(
        self,
        interaction: nextcord.Interaction,
        *,
        amount: int = nextcord.SlashOption(
            description = "amount of messages to be purged",
            required = True,
            min_value = 1,
            max_value = 1000
        )
    ) -> None:
        """This command removes the given amount of last messages from a channel."""

        self.client.Loggers.action_log(Get.log_message(
            interaction,
            "/purge",
            {"amount": str(amount)}
        ))

        self.client.Loggers.action_log(f"Guild: {interaction.guild.id} ~ Channel: {interaction.channel.id} ~ User: {interaction.user.id} ~ /purge {amount}")

        await interaction.response.defer(ephemeral=True, with_message=True)

        await interaction.channel.purge(limit=amount)

        await interaction.followup.send(embed=EmbedFunctions().success(f"Succesfully purged the last `{amount}` messages from {interaction.channel.mention}."), ephemeral=True)



def setup(client: SomiBot) -> None:
    client.add_cog(Purge(client))