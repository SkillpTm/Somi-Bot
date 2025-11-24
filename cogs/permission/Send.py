import nextcord
import nextcord.ext.commands as nextcord_C

from lib.database import db
from lib.helpers import EmbedField, EmbedFunctions
from lib.managers import Commands, Config, Lists
from lib.modules import SomiBot



class Send(nextcord_C.Cog):

    def __init__(self, client: SomiBot) -> None:
        self.client = client


    @nextcord.slash_command(
        Commands().data["send"].alias,
        Commands().data["send"].description,
        name_localizations = {country_tag: Commands().data["send"].name for country_tag in nextcord.Locale},
        default_member_permissions = nextcord.Permissions(manage_messages=True),
        integration_types = [nextcord.IntegrationType.guild_install],
        contexts = [nextcord.InteractionContextType.guild]
    )
    async def send(
        self,
        interaction: nextcord.Interaction[SomiBot],
        *,
        message: str = nextcord.SlashOption(
            Commands().data["send"].parameters["message"].name,
            Commands().data["send"].parameters["message"].description,
            required = True,
            min_length = 1,
            max_length = 1000
        ),
        channel: nextcord.TextChannel | nextcord.Thread = nextcord.SlashOption(
            Commands().data["send"].parameters["channel"].name,
            Commands().data["send"].parameters["channel"].description,
            required = False,
            channel_types = Lists().TEXT_CHANNELS
        )
    ) -> None:
        """This command allows a user to send a message with the bot."""

        channel = channel or interaction.channel

        await interaction.response.defer(ephemeral=True, with_message=True)

        message_object: nextcord.Message = await channel.send(message)
        await interaction.send(embed=EmbedFunctions().get_success_message(f"Message sent in: {channel.mention} - [Link]({message_object.jump_url})"))

        if not (command_log := interaction.guild.get_channel(int(await db.Server.COMMAND_LOG.get(interaction.guild.id) or 0))):
            return

        embed = EmbedFunctions().builder(
            color = Config().PERMISSION_COLOR,
            author = "Bot Command Log",
            author_icon = interaction.user.display_avatar.url,
            description = f"{interaction.user.mention} sent a bot message in: {channel.mention} - [Link]({message_object.jump_url})",
            fields = [
                EmbedField(
                    "Message:",
                    message,
                    False
                )
            ]
        )

        await command_log.send(embed=embed) # type: ignore


    @nextcord.slash_command(
        Commands().data["edit"].name,
        Commands().data["edit"].description,
        default_member_permissions = nextcord.Permissions(manage_messages=True),
        integration_types = [nextcord.IntegrationType.guild_install],
        contexts = [nextcord.InteractionContextType.guild]
    )
    async def edit(
        self,
        interaction: nextcord.Interaction[SomiBot],
        *,
        link: str = nextcord.SlashOption(
            Commands().data["edit"].parameters["link"].name,
            Commands().data["edit"].parameters["link"].description,
            required = True,
            min_length = 80,
            max_length = 110
        ),
        message: str = nextcord.SlashOption(
            Commands().data["edit"].parameters["message"].name,
            Commands().data["edit"].parameters["message"].description,
            required = True,
            min_length = 1,
            max_length = 1000
        )
    ) -> None:
        """This command allows a user to edit a message of the bot."""

        await interaction.response.defer(ephemeral=True, with_message=True)

        if not (message_object := await self.client.get_message_from_link(link)):
            await interaction.send(embed=EmbedFunctions().get_error_message(f"`{link}` isn't a valid message link."))
            return

        if message_object.author.id != self.client.user.id or message_object.guild.id != interaction.guild.id:
            await interaction.send(embed=EmbedFunctions().get_error_message(f"`{link}` isn't the link of a message sent by the bot in this server."))
            return

        await message_object.edit(content=message)
        await interaction.send(embed=EmbedFunctions().get_success_message(f"Message edited in: {message_object.channel.mention} - [Link]({message_object.jump_url})")) # type: ignore

        if not (command_log := interaction.guild.get_channel(int(await db.Server.COMMAND_LOG.get(interaction.guild.id) or 0))):
            return

        embed = EmbedFunctions().builder(
            color = Config().PERMISSION_COLOR,
            author = "Bot Command Log",
            author_icon = interaction.user.display_avatar.url,
            description = f"{interaction.user.mention} edited a bot message in: {message_object.channel.mention} - [Link]({message_object.jump_url})", # type: ignore
            fields = [
                EmbedField(
                    "Before:",
                    message_object.content,
                    False
                ),
                EmbedField(
                    "After:",
                    message,
                    False
                )
            ]
        )

        await command_log.send(embed=embed) # type: ignore



def setup(client: SomiBot) -> None:
    client.add_cog(Send(client))