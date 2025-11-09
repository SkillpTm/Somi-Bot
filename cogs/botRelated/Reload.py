import os

import nextcord
import nextcord.ext.commands as nextcord_C
import nextcord.ext.application_checks as nextcord_AC

from lib.helpers import EmbedFunctions, Get
from lib.managers import Commands, Config, Singleton
from lib.utilities import SomiBot



class Reload(nextcord_C.Cog):

    def __init__(self, client) -> None:
        self.client: SomiBot = client

    ####################################################################################################

    @nextcord.slash_command(
        Commands().data["reload"].name,
        Commands().data["reload"].description,
        guild_ids = [Config().SUPPORT_SERVER_ID],
        default_member_permissions = nextcord.Permissions(administrator=True),
        integration_types = [nextcord.IntegrationType.guild_install],
        contexts = [nextcord.InteractionContextType.guild]
    )
    @nextcord_AC.check(Get.interaction_by_owner())
    async def reload(self, interaction: nextcord.Interaction) -> None:
        """This command reloads the bot, it can only be executed from the owner"""

        await interaction.response.defer(ephemeral=True, with_message=True)

        self.client.is_setup = False

        Singleton.reset()
        await self.client.user.edit(username=Config().APPLICATION_NAME, avatar=nextcord.File(Config().APPLICATION_ICON_PATH), banner=nextcord.File(Config().APPLICATION_BANNER_PATH))
        self.client.change_presence(nextcord.Activity(type=nextcord.ActivityType.listening, name=Config().ACTIVITY_NAME))

        # crawl through ./cogs/ 's subfolders to reload all cogs
        for folder in os.listdir("./cogs/"):
            if not os.path.isdir(f"./cogs/{folder}/"):
                continue

            for file in os.listdir(f"./cogs/{folder}/"):
                if not file.endswith(".py"):
                    continue

                self.client.reload_extension(f"cogs.{folder}.{file[:-3]}")

        await self.client.sync_application_commands()

        self.client.is_setup = True

        await interaction.followup.send(embed=EmbedFunctions().get_success_message("The bot has been reloaded."), ephemeral=True)

        embed = EmbedFunctions().builder(
            color = Config().PERMISSION_COLOR,
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

        await self.client.get_channel(Config().SUPPORT_SERVER_LOGS_ID).send(embed=embed)



def setup(client: SomiBot) -> None:
    client.add_cog(Reload(client))