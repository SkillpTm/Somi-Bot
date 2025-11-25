import nextcord
import nextcord.ext.commands as nextcord_C

from lib.managers import Config
from lib.modules import SomiBot



class ParentCommand(nextcord_C.Cog):

    def __init__(self, client: SomiBot) -> None:
        self.client = client


    @nextcord.slash_command(
        name = "manage",
        name_localizations = {country_tag:"config" for country_tag in nextcord.Locale},
        default_member_permissions = nextcord.Permissions(manage_guild=True),
        integration_types = [nextcord.IntegrationType.guild_install],
        contexts = [nextcord.InteractionContextType.guild]
    )
    async def config(self, _interaction: nextcord.Interaction[SomiBot]) -> None:
        """Main command that does nothing for /config subcommands"""


    @nextcord.slash_command(
        name = "custom",
        default_member_permissions = nextcord.Permissions(manage_messages=True, manage_guild=True),
        integration_types = [nextcord.IntegrationType.guild_install],
        contexts = [nextcord.InteractionContextType.guild]
    )
    async def custom(self, _interaction: nextcord.Interaction[SomiBot]) -> None:
        """Main command that does nothing for /custom subcommands"""


    @nextcord.slash_command(
        name = "noti",
        name_localizations = {country_tag:"keyword" for country_tag in nextcord.Locale},
        integration_types = [nextcord.IntegrationType.guild_install],
        contexts = [nextcord.InteractionContextType.guild]
    )
    async def keyword(self, _interaction: nextcord.Interaction[SomiBot]) -> None:
        """Main command that does nothing for /keyword subcommands"""


    @nextcord.slash_command(
        name = "xp",
        name_localizations = {country_tag:"levels" for country_tag in nextcord.Locale},
        integration_types = [nextcord.IntegrationType.guild_install],
        contexts = [nextcord.InteractionContextType.guild]
    )
    async def levels(self, _interaction: nextcord.Interaction[SomiBot]) -> None:
        """Main command that does nothing for /levels subcommands"""


    @nextcord.slash_command(
        name = "lastfm",
        name_localizations = {country_tag:"lf" for country_tag in nextcord.Locale},
        integration_types = [
            nextcord.IntegrationType.user_install,
            nextcord.IntegrationType.guild_install,
        ],
        contexts = [
            nextcord.InteractionContextType.guild,
            nextcord.InteractionContextType.bot_dm,
            nextcord.InteractionContextType.private_channel,
        ]
    )
    async def lastfm(self, _interaction: nextcord.Interaction[SomiBot]) -> None:
        """Main command that does nothing for /lf subcommands"""


    @nextcord.slash_command(
        name = "alarm",
        name_localizations = {country_tag:"reminder" for country_tag in nextcord.Locale},
        integration_types = [
            nextcord.IntegrationType.user_install,
            nextcord.IntegrationType.guild_install,
        ],
        contexts = [
            nextcord.InteractionContextType.guild,
            nextcord.InteractionContextType.bot_dm,
            nextcord.InteractionContextType.private_channel,
        ]
    )
    async def reminder(self, _interaction: nextcord.Interaction[SomiBot]) -> None:
        """Main command that does nothing for /reminder subcommands"""


    @nextcord.slash_command(
        name = "sudo",
        guild_ids = [Config().SUPPORT_SERVER_ID],
        default_member_permissions = nextcord.Permissions(administrator=True),
        integration_types=[nextcord.IntegrationType.guild_install],
        contexts=[nextcord.InteractionContextType.guild]
    )
    async def sudo(self, _interaction: nextcord.Interaction[SomiBot]) -> None:
        """Main command that does nothing for /sudo subcommands"""



def setup(client: SomiBot) -> None:
    client.add_cog(ParentCommand(client))