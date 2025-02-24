####################################################################################################

import nextcord
import nextcord.ext.commands as nextcord_C
import nextcord.ext.application_checks as nextcord_AC

####################################################################################################

from lib.db_modules import ConfigDB
from lib.modules import Checks, EmbedFunctions, Get
from lib.utilities import TEXT_CHANNELS, SomiBot



class ConfigHiddenChannels(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    from lib.utilities.main_commands import config

    ####################################################################################################

    @config.subcommand(name = "hidden-channels", description = "add/remove a hidden-channel to this server")
    @nextcord_AC.check(Checks().interaction_in_guild and Checks().interaction_not_by_bot())
    async def config_hidden_channels(
        self,
        interaction: nextcord.Interaction,
        *,
        action: str = nextcord.SlashOption(
            description="which action do you want to take",
            required=True,
            choices=["Add", "Remove"]
        ),
        channel: nextcord.abc.GuildChannel = nextcord.SlashOption(
            channel_types=TEXT_CHANNELS,
            description="the channel to be added/removed",
            required=False)
        ) -> None:
        """This command adds a custom command to the server's custom commands"""

        if not channel:
            channel = interaction.channel

        self.client.Loggers.action_log(Get().interaction_log_message(
            interaction,
            "/config hidden-channels",
            {"action": action, "channel": str(channel.id)}
        ))

        await interaction.response.defer(ephemeral=True, with_message=True)


        if action == "Add":
            if not await self.addChannel(interaction, channel):
                return
            
            mod_action = f"{interaction.user.mention} added: {channel.mention} as a hidden-channel."   

        elif action == "Remove":
            if not await self.removeChannel(interaction, channel):
                return

            mod_action = f"{interaction.user.mention} removed: {channel.mention} from the hidden-channels."  


        audit_log_id: int = await ConfigDB(interaction.guild.id, "AuditLogChannel").get_list(interaction.guild)

        if not audit_log_id:
            return

        embed = EmbedFunctions().builder(
            color = self.client.MOD_COLOR,
            author = "Mod Activity",
            author_icon = interaction.user.display_avatar,
            footer = "DEFAULT_KST_FOOTER",
            fields = [
                [
                    "/config default-role:",
                    mod_action,
                    False
                ]
            ]
        )

        await interaction.guild.get_channel(audit_log_id).send(embed=embed)

    ####################################################################################################

    @staticmethod
    async def addChannel(
        interaction: nextcord.Interaction,
        channel: nextcord.abc.GuildChannel
    ) -> bool:
        "adds or doesn't add the role indicated by the output bool"

        added = ConfigDB(interaction.guild.id, "HiddenChannels").add(channel.id)

        if not added:
            await interaction.followup.send(embed=EmbedFunctions().error(f"{channel.mention} is already a hidden-channel.\nTo get a list of all the hidden-channels use `/config info`."), ephemeral=True)
            return added

        await interaction.followup.send(embed=EmbedFunctions().success(f"{channel.mention} has been added to the hidden-channels."), ephemeral=True)
        return added

    ####################################################################################################

    @staticmethod
    async def removeChannel(
        interaction: nextcord.Interaction,
        channel: nextcord.abc.GuildChannel
    ) -> bool:
        "removes or doesn't remove the channel indicated by the output bool"

        deleted = ConfigDB(interaction.guild.id, "HiddenChannels").delete(channel.id)

        if not deleted:
            await interaction.followup.send(embed=EmbedFunctions().error(f"{channel.mention} isn't a hidden-channel.\nTo get a list of all the hidden-channels use `/config info`."), ephemeral=True)
            return deleted

        await interaction.followup.send(embed=EmbedFunctions().success(f"{channel.mention} has been removed from the hidden-channels."), ephemeral=True)
        return deleted




def setup(client: SomiBot) -> None:
    client.add_cog(ConfigHiddenChannels(client))