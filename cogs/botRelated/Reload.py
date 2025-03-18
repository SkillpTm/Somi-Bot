import nextcord
import nextcord.ext.commands as nextcord_C
import nextcord.ext.application_checks as nextcord_AC
import os

from lib.modules import EmbedFunctions, Get
from lib.utilities import SomiBot



class Reload(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    @nextcord.slash_command(
        name = "reload",
        description = "reload the entire bot",
        guild_ids = [SomiBot.SUPPORT_SERVER_ID],
        default_member_permissions = nextcord.Permissions(administrator=True),
        integration_types = [nextcord.IntegrationType.guild_install],
        contexts = [nextcord.InteractionContextType.guild]
    )
    @nextcord_AC.check(Get.interaction_by_owner())
    async def reload(self, interaction: nextcord.Interaction) -> None:
        """This command reloads the bot, it can only be executed from the owner"""

        self.client.Loggers.action_log(Get.log_message(interaction, "/reload"))

        await interaction.response.defer(ephemeral=True, with_message=True)


        # crawl through ./cogs/ 's subfolders to reload all cogs
        for folder in os.listdir(f"./cogs/"):
            if not os.path.isdir(f"./cogs/{folder}/"):
                continue
            
            for file in os.listdir(f"./cogs/{folder}/"):
                if not file.endswith(".py"):
                    continue

                self.client.reload_extension(f"cogs.{folder}.{file[:-3]}")


        await self.client.sync_application_commands()
                    
        await interaction.followup.send(embed=EmbedFunctions().get_success_message("The bot has been reloaded."), ephemeral=True)


        embed = EmbedFunctions().builder(
            color = self.client.MOD_COLOR,
            author = "Dev Activity",
            author_icon = interaction.user.display_avatar.url,
            fields = [
                [
                    "/reload:",
                    f"{interaction.user.mention} reloaded the bot!",
                    False
                ]
            ]
        )

        await self.client.get_channel(self.client.SUPPORT_SERVER_LOGS_ID).send(embed=embed)



def setup(client: SomiBot) -> None:
    client.add_cog(Reload(client))