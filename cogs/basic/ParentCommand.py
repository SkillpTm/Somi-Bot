import nextcord
import nextcord.ext.commands as nextcord_C

from lib.utilities import SomiBot



class ParentCommand(nextcord_C.Cog):
    """This cog just holds the parent slash commands for all subcommands"""

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    @nextcord.slash_command(
        name = "manage",
        default_member_permissions = nextcord.Permissions(manage_guild=True),
        name_localizations = {country_tag:"config" for country_tag in nextcord.Locale},
        integration_types = [nextcord.IntegrationType.guild_install],
        contexts = [nextcord.InteractionContextType.guild]
    )
    async def config(self, interaction: nextcord.Interaction) -> None:
        pass

    ####################################################################################################

    @nextcord.slash_command(
        name = "custom",
        default_member_permissions = nextcord.Permissions(manage_messages=True, manage_guild=True),
        integration_types = [nextcord.IntegrationType.guild_install],
        contexts = [nextcord.InteractionContextType.guild]
    )
    async def custom(self, interaction: nextcord.Interaction) -> None:
        pass

    ####################################################################################################


    @nextcord.slash_command(
        name = "noti",
        name_localizations = {country_tag:"keyword" for country_tag in nextcord.Locale},
        integration_types = [nextcord.IntegrationType.guild_install],
        contexts = [nextcord.InteractionContextType.guild]
    )
    async def keyword(self, interaction: nextcord.Interaction) -> None:
        pass

    ####################################################################################################

    @nextcord.slash_command(
        name = "xp",
        name_localizations = {country_tag:"levels" for country_tag in nextcord.Locale},
        integration_types = [nextcord.IntegrationType.guild_install],
        contexts = [nextcord.InteractionContextType.guild]
    )
    async def levels(self, interaction: nextcord.Interaction) -> None:
        pass

    ####################################################################################################

    @nextcord.slash_command(
        name = "lastfm",
        name_localizations = {country_tag:"lf" for country_tag in nextcord.Locale},
    )
    async def lastfm(self, interaction: nextcord.Interaction) -> None:
        pass

    ####################################################################################################

    @nextcord.slash_command(
        name = "alarm",
        name_localizations = {country_tag:"reminder" for country_tag in nextcord.Locale}
    )
    async def reminder(self, interaction: nextcord.Interaction) -> None:
        pass



def setup(client: SomiBot) -> None:
    client.add_cog(ParentCommand(client))