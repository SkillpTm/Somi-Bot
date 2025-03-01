import nextcord
import nextcord.ext.commands as nextcord_C
import nextcord.ext.application_checks as nextcord_AC

from lib.db_modules import ConfigDB
from lib.modules import Checks, EmbedFunctions, Get
from lib.utilities import TEXT_CHANNELS, SomiBot



class Send(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    @nextcord.slash_command(
        name = "say",
        description = "sends a message in a channel",
        default_member_permissions = nextcord.Permissions(manage_messages=True),
        name_localizations = {country_tag:"send" for country_tag in nextcord.Locale},
        integration_types = [nextcord.IntegrationType.guild_install],
        contexts = [nextcord.InteractionContextType.guild]
    )
    @nextcord_AC.check(Checks.interaction_not_by_bot() and Checks.interaction_in_guild())
    async def send(
        self,
        interaction: nextcord.Interaction,
        *,
        message: str = nextcord.SlashOption(
            description = "the message to be send by the bot",
            required = True,
            min_length = 1,
            max_length = 1000
        ),
        channel: nextcord.abc.GuildChannel = nextcord.SlashOption(
            channel_types = TEXT_CHANNELS,
            description = "channel in which the message will be send",
            required = False
        )
    ) -> None:
        """This command allows a user to send a message with the bot."""

        if not channel:
            channel = interaction.channel

        self.client.Loggers.action_log(Get.log_message(
            interaction,
            "/send",
            {"message": message, "channel": (channel.id)}
        ))

        await interaction.response.defer(ephemeral=True, with_message=True)

        message_object: nextcord.Message = await channel.send(message)
        await interaction.followup.send(embed=EmbedFunctions().success(f"Message sent in: {channel.mention} - [Link]({message_object.jump_url})"), ephemeral=True)


        audit_log_id: int = await ConfigDB(interaction.guild.id, "AuditLogChannel").get_list(interaction.guild)

        if not audit_log_id:
            return

        embed = EmbedFunctions().builder(
            color = self.client.MOD_COLOR,
            author = "Mod Activity",
            author_icon = interaction.user.display_avatar,
            description = f"{interaction.user.mention} sent a bot message in: {channel.mention} - [Link]({message_object.jump_url})",
            footer = "DEFAULT_KST_FOOTER",
            fields = [
                [
                    "Message:",
                    message,
                    False
                ]
            ]
        )

        await interaction.guild.get_channel(audit_log_id).send(embed=embed)

    ####################################################################################################

    @nextcord.slash_command(
        name = "edit",
        description = "edits a bot message in a channel",
        default_member_permissions = nextcord.Permissions(manage_messages=True),
        integration_types = [nextcord.IntegrationType.guild_install],
        contexts = [nextcord.InteractionContextType.guild]
    )
    @nextcord_AC.check(Checks.interaction_not_by_bot() and Checks.interaction_in_guild())
    async def edit(
        self,
        interaction: nextcord.Interaction,
        *,
        message_id: str = nextcord.SlashOption(
            description = "ID of the message to be edited",
            required = True,
            min_length = 18,
            max_length = 19
        ),
        message: str = nextcord.SlashOption(
            description = "the new message to be edited by the bot",
            required = True,
            min_length = 1,
            max_length = 1000
        )
    ) -> None:
        """This command allows a user to edit a message of the bot."""

        await interaction.response.defer(ephemeral=True, with_message=True)

        message_object: nextcord.Message = None

        if not message_id.isdigit():
            await interaction.followup.send(embed=EmbedFunctions().error(f"`{message_id}` isn't a valid message ID."), ephemeral=True)
            return

        # check all channels for in which one the message was send
        for channel in await interaction.guild.fetch_channels():
            if not channel.type in TEXT_CHANNELS:
                continue

            try:
                message_object = await channel.fetch_message(int(message_id))
                correct_channel = channel
                break
            except nextcord.NotFound:
                pass

        if not message_object or message_object.author.id != self.client.user.id:
            await interaction.followup.send(embed=EmbedFunctions().error(f"`{message_id}` isn't an id of a message sent by the bot in this server."), ephemeral=True)
            return

        self.client.Loggers.action_log(Get.log_message(
            interaction,
            "/edit",
            {"message_id": str(message_id), "old message": message_object.content, "new message": message}
        ))

        await message_object.edit(content=message)
        
        await interaction.followup.send(embed=EmbedFunctions().success(f"Message edited in: {correct_channel.mention} - [Link]({message_object.jump_url})"), ephemeral=True)


        audit_log_id: int = await ConfigDB(interaction.guild.id, "AuditLogChannel").get_list(interaction.guild)

        if not audit_log_id:
            return

        embed = EmbedFunctions().builder(
            color = self.client.MOD_COLOR,
            author = "Mod Activity",
            author_icon = interaction.user.display_avatar,
            description = f"{interaction.user.mention} edited a bot message in: {correct_channel.mention} - [Link]({message_object.jump_url})",
            footer = "DEFAULT_KST_FOOTER",
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

        await interaction.guild.get_channel(audit_log_id).send(embed=embed)



def setup(client: SomiBot) -> None:
    client.add_cog(Send(client))