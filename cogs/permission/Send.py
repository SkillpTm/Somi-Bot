import nextcord
import nextcord.ext.commands as nextcord_C

from lib.dbModules import DBHandler
from lib.helpers import EmbedFunctions
from lib.managers import Commands, Config, Lists
from lib.utilities import SomiBot



class Send(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

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
        interaction: nextcord.Interaction,
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
        await interaction.followup.send(embed=EmbedFunctions().get_success_message(f"Message sent in: {channel.mention} - [Link]({message_object.jump_url})"), ephemeral=True)

        if not (audit_log := interaction.guild.get_channel(await (await DBHandler(self.client.database, server_id=interaction.guild.id).server()).audit_log_get() or 0)):
            return

        embed = EmbedFunctions().builder(
            color = Config().PERMISSION_COLOR,
            author = "Mod Activity",
            author_icon = interaction.user.display_avatar.url,
            description = f"{interaction.user.mention} sent a bot message in: {channel.mention} - [Link]({message_object.jump_url})",
            fields = [
                [
                    "Message:",
                    message,
                    False
                ]
            ]
        )

        await audit_log.send(embed=embed)

    ####################################################################################################

    @nextcord.slash_command(
        Commands().data["edit"].name,
        Commands().data["edit"].description,
        default_member_permissions = nextcord.Permissions(manage_messages=True),
        integration_types = [nextcord.IntegrationType.guild_install],
        contexts = [nextcord.InteractionContextType.guild]
    )
    async def edit(
        self,
        interaction: nextcord.Interaction,
        *,
        message_id: str = nextcord.SlashOption(
            Commands().data["edit"].parameters["message_id"].name,
            Commands().data["edit"].parameters["message_id"].description,
            required = True,
            min_length = 18,
            max_length = 19
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

        message_object: nextcord.Message = None

        if not message_id.isdigit():
            await interaction.followup.send(embed=EmbedFunctions().get_error_message(f"`{message_id}` isn't a valid message ID."), ephemeral=True)
            return

        # check all channels for in which one the message was send
        for channel in await interaction.guild.fetch_channels():
            if not channel.type in Lists().TEXT_CHANNELS:
                continue

            try:
                message_object = await channel.fetch_message(int(message_id))
                correct_channel = channel
                break
            except nextcord.NotFound:
                pass

        if not message_object or message_object.author.id != self.client.user.id:
            await interaction.followup.send(embed=EmbedFunctions().get_error_message(f"`{message_id}` isn't an id of a message sent by the bot in this server."), ephemeral=True)
            return

        await message_object.edit(content=message)

        await interaction.followup.send(embed=EmbedFunctions().get_success_message(f"Message edited in: {correct_channel.mention} - [Link]({message_object.jump_url})"), ephemeral=True)

        if not (audit_log := interaction.guild.get_channel(await (await DBHandler(self.client.database, server_id=interaction.guild.id).server()).audit_log_get() or 0)):
            return

        embed = EmbedFunctions().builder(
            color = Config().PERMISSION_COLOR,
            author = "Mod Activity",
            author_icon = interaction.user.display_avatar.url,
            description = f"{interaction.user.mention} edited a bot message in: {correct_channel.mention} - [Link]({message_object.jump_url})",
            fields = [
                [
                    "Before:",
                    message_object.content,
                    False
                ],

                [
                    "After:",
                    message,
                    False
                ]
            ]
        )

        await audit_log.send(embed=embed)



def setup(client: SomiBot) -> None:
    client.add_cog(Send(client))