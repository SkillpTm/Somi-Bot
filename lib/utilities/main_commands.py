import nextcord

from lib.utilities.SomiBot import SomiBot

client = SomiBot()

####################################################################################################

@client.slash_command(
    name='manage',
    default_member_permissions=nextcord.Permissions(manage_guild=True),
    name_localizations = {country_tag:"config" for country_tag in nextcord.Locale},
    integration_types = [nextcord.IntegrationType.guild_install],
    contexts = [nextcord.InteractionContextType.guild]
)
async def config(self, interaction: nextcord.Interaction) -> None:
    pass

####################################################################################################

@client.slash_command(
    name='custom',
    default_member_permissions=nextcord.Permissions(manage_messages=True, manage_guild=True),
    integration_types = [nextcord.IntegrationType.guild_install],
    contexts = [nextcord.InteractionContextType.guild]
)
async def custom(self, interaction: nextcord.Interaction) -> None:
    pass

####################################################################################################


@client.slash_command(
    name='noti',
    name_localizations = {country_tag:"keyword" for country_tag in nextcord.Locale},
    integration_types = [nextcord.IntegrationType.guild_install],
    contexts = [nextcord.InteractionContextType.guild]
)
async def keyword(self, interaction: nextcord.Interaction) -> None:
    pass

####################################################################################################

@client.slash_command(
    name='xp',
    name_localizations = {country_tag:"levels" for country_tag in nextcord.Locale},
    integration_types = [nextcord.IntegrationType.guild_install],
    contexts = [nextcord.InteractionContextType.guild]
)
async def levels(self, interaction: nextcord.Interaction) -> None:
    pass

####################################################################################################

@client.slash_command(name='lf')
async def lastfm(self, interaction: nextcord.Interaction) -> None:
    pass

####################################################################################################

@client.slash_command(
    name='alarm',
    name_localizations = {country_tag:"reminder" for country_tag in nextcord.Locale}
)
async def reminder(self, interaction: nextcord.Interaction) -> None:
    pass